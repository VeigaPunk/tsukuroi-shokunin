# Round 48 — lesson (tsukuroi, hyaku run 10, attempt 2)

author: tsukuroi L1 (`TsukuroiR48a2`), 2026-10-28. Base `5fdf062f969292736e36513e39f98b1b8de43635`.
Freeze `ae99f021b76f8eb1c8805d32d80644464afb1ff6`; counted wave `w2`, 71 seats. Attempt 1's w1 is void incident evidence only; its outputs are not scored. Claims C1 operability / C2 depth / C3 calibration: `SCORECARD.md`, Round 48 declaration and outcome.

## Outcome (author-side; non-author closure pending)

- **C1 operability — PASS.** Frozen counter `tools/score-selftest-tmpdir-r48.py` at the frozen census blob `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426` returned `PASS`, all six legs at target (after receipt `.ufo/waves/round-48/after/c1-final.json`). The w2 reviewers and attacks found the core fd-alias behavior holds. Defects remain: the frozen census comment at line 415 inaccurately says the harness builds a `/tmp` fixture tree, and the fixed fd band 240–249 exhausts fail-closed without a summary (w2 `TExecLint.md`, `TExecFdHold.md`); these do not change the frozen C1 predicate. No axis is claimed harmed.
- **C2 depth — FAIL (honest stop).** Frozen counter `tools/check-scrub-admission-r48.py` at integrated revision returned `structural_ok=1, quotes_ok=3, verdicts_ok=1, marks_ok=0, FAIL` (`.ufo/waves/round-48/after/c2-final.json`). GR1 received one counted `partly`, GR2 two `partly`; only GR3 qualified. The frozen entry lacks all three round-48 marks. No admission mark, knowledge credit, or depth-score increase is claimed. The counted reviews identify several GR1/GR2 overstatements; preserve the exact proposed amendments in their reports, not by rewriting the frozen rows.
- **C3 calibration — PASS.** Before restatement, `check-self-assessment.py` found 3 mismatches (K10 lessons 70→71, K13 census 164→166, K17 capability count 164→166). At `8717d8e9ecbbf776fd80b602a74218e51f7b11a8`, `python3 tools/check-self-assessment.py --revision <REV>` → checked 27, mismatches 0, PASS (`.ufo/waves/round-48/after/c3-final.json`).

## Gate

| ID | Decision | Source opened / evidence | Located quote (≤25 words) | Lesson action |
|---|---|---|---|---|
| S251 | admit / re-open | Linux man-pages proc_pid_fd(5), fetched live by seat SScoutProcFd 2026-10-28; sha256 `3a50ddef6f2f3a4f1139dcef3299a5eadf8fc96514df9fcb329a3bffd47ff27e`, matches the S251 pin | `each fd entry is a symbolic link to the actual file` | Supports the `/proc/self/fd/<n>` alias mechanism; row's used-by now includes this lesson. |
| S253 | admit | POSIX.1-2024 Shell Command Language §2.6.5 / §2.2.3, fetched live by seat SScoutReject on 2026-10-28, sha256 `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd` | `Enclosing characters in double-quotes ("") shall preserve the literal value of all characters within the double-quotes` | New primary source row; the lane lesson records why quoting/indirection preserves the path value relevant to C1. |
| S254 | reject | Unix & Linux Stack Exchange Q131766, stackprinter export fetched 2026-10-28, sha256 `b8798c059aa3326300f4ecdcf8135428f1586af8c0a3cebb49da87353ec4e6a8` (direct page fetch returned 403) | `Always use double quotes around variable substitutions and command substitutions` | Reject tier-C gloss: S253 states the rule normatively and S252 covers mktemp's directory selection; flip if a future entry needs a worked TMPDIR/mktemp failure or distinct non-normative heuristic. Rejection retained as S254. |
| S255 | admit | GNU Bash Reference Manual 5.3, Redirections, fetched live by seat SScoutBashRedir 2026-10-28; sha256 `78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b` | `Redirections using file descriptors greater than 9 should be used with care` | New primary row documents the fd>9 caution relevant to the fixed 240–249 band; the seat's empirical check reports the live shell script descriptor and collision handling. |

SOURCES: start census exit 0 in `.ufo/waves/round-48/before/sources-census-start.txt`; final census exit 0 in `.ufo/waves/round-48/after/sources-census-end.txt`. IDs S001–S252 existed at start; S253 admitted, S254 rejected and S255 admitted this round. No shokuknow package knowledge entry was assimilated (claims frozen; no package entry fits without widening); `merge/tsukuroi` remains read-only. S240/S251/S250 re-opened this round; S240 and S251 used-by changes are old→new below. Frontier: S253 POSIX.1-2024 and S255 Bash manual opened and cited here; no package assimilation was done.

## Mistakes

| ID | Class | Evidence | Captured-by | Fix (and how it is shown able to fail) |
|---|---|---|---|---|
| R48-W1-PRE-FREEZE-DISPATCH | process — invalid 32-seat w1 dispatched before claims, counter or controls were frozen, with stale base | `.ufo/waves/round-48/w1.ready`, `w1-spec.json`, `w1-dispatch.json`; explicit orchestrator incident ruling; `w1/INCIDENT.md` | No pre-ready freeze gate existed; captured by the orchestrator stop and round-48 attempt-2 process rule | Attempt 2 froze before w2; K0 control is committed, and the validator reports 71 seats. Keep w1 untouched and void; verify by reading the stamped ready/spec and freeze commit order. |
| R47-C2-TMPDIR-FALLBACK | scratch-scope defect — round-47 fallback redirected a spaced TMPDIR fixture to `/tmp` | Base blob `tools/tsukuroi-census.sh` at `5fdf062f`, `st_base=/tmp`; C1 battery K0 and K2 (`battery-summary-r48-c1.jsonl`) show `loc_ok=3` | R47 C2 kill rule caught it only after the bad fix landed | R48 uses a directory fd alias inside TMPDIR; K2 restores the fallback and fails `loc_ok` and `static_ok`. |
| R48-C2-BIND-VANISHES-NEGATIVE | counter design — first draft's `bind` dropped a short/self-contradicting negative as unbound, so the negative could vanish | `controls/battery-c2.py` K3/K3b/K3c/K3d and `battery-summary-r48-c2.jsonl` | Pre-data battery caught the first draft before the freeze | Changed `bind` to retain verdicts and moved citation/length gating to credit; each negative control returns `verdicts_ok=2`, not 3. |
| R48-C1-BARE-PASS-NEEDLE | counter design — first C1 counter searched stdout for bare `PASS`, matching ordinary case lines during TERM | frozen `tools/score-selftest-tmpdir-r48.py` now looks for the summary prefix; K3 TERM-mutant fails `term_ok`, K-pass succeeds | Pre-data K-pass outcome and K3 mutant | Match the unique summary line, not a substring; battery receipts prove the defect is caught. |
| R48-C1-STALE-TMPDIR-COMMENT | documentation drift — census comment still says selftest builds a `/tmp` fixture tree, contradicting the actual TMPDIR behavior | frozen `tools/tsukuroi-census.sh:415`; independent `TExecLint.md` and `TExecStrace.md` | Not covered by the frozen C1 static leg (comments are excluded) | Next round correct the comment; routed, not patched after this freeze. |

## Re-opened registry rows / touched cells (old → new)
| Row | Old → new | Evidence / action |
|---|---|---|
| S240 | used-by `corpus/knowledge/btrfs-scrub-record-r43.md, corpus/knowledge/btrfs-scrub-record-r44.md` → add `corpus/lessons/round-48.md` | Live re-open 2026-10-28, byte-identical digest and ioctl.c:3190 quote above. |
| S251 | used-by `corpus/knowledge/census-identity-r46.md` → add `corpus/lessons/round-48.md` | Live re-open by SScoutProcFd; digest matches S251 pin and the symlink quote is in its report. |
| S253 | new admitted row, used-by `corpus/lessons/round-48.md` | Opened live by SScoutReject; source/quote/digest above. |
| S254 | new rejected row, used-by `—` | Opened live by SScoutReject; decision and flip condition above. |
| S255 | new admitted row, used-by `corpus/lessons/round-48.md` | Opened live by SScoutBashRedir; 2026-10-28 digest and located fd>9 caveat above. |

## Counters and limits

The C2 result is a frozen-counter FAIL; do not infer that all three rows passed from independent seat prose. The counter's row result is not an admission mark and no SKILL/README/knowledge admission marker is added. C1 is measured PASS; C3 is measured PASS at `67dfd8aa` (`checked 27, mismatches 0`), and this lesson is included in the 72-file K10 count on the next commit. `TExecStrace` under a spaced TMPDIR traced zero `/tmp`, `/var/tmp`, `/dev/shm` paths in the successful run; its stressed strace run exposed one unrelated host-source assertion (receipt says 165/166), while the untraced controls passed. `TExecEdgeChars` exercised the requested unusual TMPDIR values and records the no-injection / no-silent-fallback evidence. `TExecFdHold` found exhaustion/low-RLIMIT paths can exit 1 without a summary; fail-closed, but routed for improved diagnostic and targeted test. No tool install/update. No L0 question.
