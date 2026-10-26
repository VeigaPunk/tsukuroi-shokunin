VERDICT: supports

Seat C1RevIntegration (L2, round 43 wave 2, item C1-F6). Reviewed `git diff 717b716a8943151ace8657e0ca23d7d9b8434f26 8acf0b022586a0f3164c77659fb96ba5f90949b6 -- tools/boot-chain-audit.sh SKILL.md` for C1: the added `R43-C1-missing-start-point-silent` case and the SKILL section "Boot-input freshness under pipefail — round 43" plus the registry row `bootinputs-r43`. No inaccuracy found against the receipts; all numbers and claims checked below hold. Findings are ordered by severity; only notes (N1-N4) follow the verified claims.

## 1. The added selftest case (tools/boot-chain-audit.sh:1238-1239 at the tip)

Added lines (diff hunk at :1235-1238):

```bash
    got=$(inputs_newer_than 2000 "$bi/missing" "$bi/old" 2>&1)
    st_check 'R43-C1-missing-start-point-silent' 0 "$got"
```

- Does it test what its name says? Yes. With a missing start point (`$bi/missing`) and nothing newer after it, it asserts the function's combined stdout+stderr is exactly `0`: correct decision plus silent stderr (the `2>&1` captures find's diagnostics). Verified red on the drop-`2>/dev/null` mutant (mutant (c)): `FAIL total=49 failed=1`, failing only `R43-C1-missing-start-point-silent` with `expected [0] got [find: '…/bootinputs/missing': No such file or directory\n0]`; pristine tip passes `PASS total=49 failed=0`. Mutant (b) (drop `-quit`) still survives (`PASS total=49`), mutant (a) (decision inverted) is killed by all four R43-C1 cases (`failed=4`) — attribution clean. The kill claim in SKILL.md:3987-3988 ("it kills the drop-`2>/dev/null` mutant that survived the first three, wave-1 `C1MutFix` (c), `C1MutSelftest`") is confirmed: both wave-1 reports record (c) as surviving the first three cases.
- Locale: no dependence. The assertion is exact equality to `0`; any localized find diagnostic is non-empty and fails the mutant. Outcome cannot flip with locale.
- umask: no dependence. The fixture uses `mkdir -p`/`touch` paths; no permission-sensitive path is involved, so the case's verdict is umask-invariant (an extreme umask makes `$bi/d` unreadable, which still yields `0` and still catches the mutant's stderr leak).
- TMPDIR: no dependence beyond the whole selftest's need for a writable `TMPDIR` (fixtures under `$T=$(mktemp -d "${TMPDIR:-/tmp}/…")`, boot-chain-audit.sh:888). The case itself uses only `$bi` paths under `$T`.
- N2 (portability note, not an inaccuracy): the kill power assumes `find` reports a missing start point on stderr with a non-empty message (confirmed `findusr/bin/find`, GNU findutils 4.11.0-modified). A find that silently skipped missing start points would make the case pass on mutant (c) too. The capture covers the none-newer shape; the deep-newer shape (case 2) has no stderr capture, so the kill property is demonstrated for the tested shape only — exactly the declared intent.

## 2. SKILL section "Boot-input freshness under pipefail — round 43" (SKILL.md:3958-4000)

Every number and claim checked against `.ufo/waves/round-43/` receipts:

| Claim (line) | Evidence | Verdict |
|---|---|---|
| Routed defect R42-C1-COUNTER-AMEND item 5, §6 (:3960-3962) | `corpus/lessons/round-42-verifier-spotcheck.md` §6 (line 189) item 4, bullet 5 names the `tools/boot-chain-audit.sh:480-487` fail-open; round-42 section quote "Not fixed here (routed)" at SKILL.md:3893 | holds |
| Base/fix ids; "one selftest case added at the round-43 integration commit" (:3963-3964) | `git diff 717b716 8acf0b -- tools/boot-chain-audit.sh` shows exactly one added `st_check`; integration commit 9b974f2a message "R43-C1 stderr selftest case (49)" | holds |
| Base pipeline `find <8 start points> … -print -quit 2>/dev/null \| grep -q .`, prints 1 only on pipeline success (:3966-3968) | base bytes :480-487 (w1/C1ExecHandRepro.md §1 verbatim quote); C1ExecHandRepro transcript `BASE_PIPELINE_RC=1` with find listing a newer input | holds |
| find exits 1 on missing/unreadable start point; pipefail masks the match; 0 feeds BOOTED-OBSERVED gate `newer = 0` (:3968-3970) | C1ExecHandRepro.md §3 (`FIND_RC=1`, `unreadable-dir` leg rc=1, gate conjunct at base :761 / fix :770) | holds |
| Table row 1: six `miss/etc/*-newer` cases, expected 1 got 0 (:3974) | `before/c1-before.jsonl` wrong list contains exactly six `miss/etc/*-newer` ids (fstab, crypttab, mkinitcpio.conf, mkinitcpio.conf.d, default/limine, limine-snapper-sync.conf), each `expect 1 got 0` | holds |
| Table row 2: `unreadable-dir-modules-newer` expect 1 got 0; mode 0700 not the caller's (:3975) | same receipt; `make_cases` builds `/etc/mkinitcpio.conf.d/<word>` mode 0o700 under inside-ns uid 0, scored at setpriv uid 1000 (score-bootinputs-r43.py:210-212, :84) | holds |
| Table row 3: `multi-miss-deep-modules-newer` (2-4 missing, deep modules file) expect 1 got 0 (:3976) | same receipt; `make_cases` miss=2-4 ETC points, depth 3 modules carrier (:207-209) | holds |
| Rule / K9 / K10 (:3978-3982) | K9 variant `{ find … || true; } | grep -q .` and K10 `-e` pre-filter in `run_controls_c1.py:71-78`; battery summary K9 PASS, K10 FAIL | holds |
| Selftest counts 45 → 48 at 717b716, 49 at integration (:3986-3987) | `before/c1-before.jsonl` `total=45`; `after/c1-after-717b716.jsonl` `total=48`, `selftest_r43 3`; my pristine tip run `PASS total=49 failed=0`, counter `selftest_r43 4` | holds |
| Counter predicate and sha256 `886f92c8…e10f` (:3990-3991) | `sha256sum tools/score-bootinputs-r43.py` = `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f`; `PREDICATE` constant :66-67 | holds |
| Base FAIL correct 8; 717b716 PASS correct 16; re-runs (:3992) | `before/c1-before.jsonl` (correct 8); `after/c1-after-717b716.jsonl` (correct 16); `w1/C1ExecRerun.md` (5× after PASS byte-identical, 2× base FAIL correct 8) | holds |
| Controls: K0-K6, K10 FAIL; K8, K9 PASS; K7 mount-gated PASS recorded; `should_fail_accepted 0, control_accepted 1` (:3992-3995) | `controls/battery-summary-c1.jsonl` (K0-K6,K10 FAIL; K7 PASS recorded; K8,K9 PASS; summary line 2) | holds |
| Channels: mount table, uid_map, `/mnt/bca-lib.sh`, cwd open (wave-1 C1CritChannels) (:3994-3995) | `w1/C1CritChannels.md` documents all four (and more, see N1); counter `channels_open` lists the first three | holds |
| Limits: verdict-line/btime/btime−1/start-point-membership gaps (:3997-4000) | `w1/C1MutFix.md` mutants j, i, e and the counter-scores-value note; `w1/C1ExecHandRepro.md` §1 gate plumbing | holds |

## 3. Registry row `bootinputs-r43` (SKILL.md:4111)

Entry command, verdict map (0 predicate / 1 any conjunct fails / 2 could-not-evaluate), "none: no self-test mode", the 16 namespace cases + live leg + own `--selftest` as measurement, the controls pointer `run_controls_c1.py`, pinned counter sha256 `886f92c8…e10f`, caller uid/gid via `/etc/subuid` + `setpriv`, mount-table/uid_map/script-path declared open, and write scope (private `--scratch`, removed on exit/SIGINT/SIGTERM, tmpfs only inside its `unshare -m`, revision read via `git show`) all match `tools/score-bootinputs-r43.py` (argparse :237-242, die(2) :121-123, run return 0/1 :344, INNER :70-118, signal handlers :247-251, `git show` :263) and the receipts. Registry coverage at the tip is green: `check-registry-coverage.py --revision 8acf0b…` from the fixture clone → `PASS`, 68/68 registered, findings 0 — confirming the historical 66/68 F1 claim (SKILL.md:4040) is closed.

## 4. Verification performed (receipts in .ufo/waves/round-43/w2/C1RevIntegration/)

- `bca-tip.sh` (sha256 `77c80be8…9141ad`) = `git show 8acf0b…:tools/boot-chain-audit.sh`.
- Pristine tip `--selftest`: `PASS total=49 failed=0`, rc 0.
- Mutant (c) (drop ` 2>/dev/null`): `FAIL total=49 failed=1`, only `R43-C1-missing-start-point-silent` red.
- Mutant (b) (drop `-quit`): `PASS total=49`, rc 0.
- Mutant (a) (invert decision): `FAIL total=49 failed=4`.
- Frozen counter at 8acf0b (fixture clone `--lane`, `--scratch`): `verdict PASS`, cases 16, correct 16, identity_ok 1, live_agree 1, `selftest_line "…PASS total=49 failed=0"`, `selftest_r43 4`, exit 0.
- `check-registry-coverage.py --revision 8acf0b…`: `PASS`, 68/68, findings 0.

## 5. Notes (no falsification)

- N1 (low): the channels sentence (:3994-3995) lists four channels; `w1/C1CritChannels.md` documents additional open channels (identity/env/stdin/timing, fixture shapes). The sentence is accurate but could be read as exhaustive; "e.g." would be tighter. Not a factual error.
- N2: portability caveat of the new case (Section 1).
- N3 (low): `selftest_r43` counts `st_check 'R43-C1-` lines in the script source, not executed outcomes (score-bootinputs-r43.py:332); the declared predicate and receipts match, and `selftest_pass` covers a failing case. Note only.
- N4 (low): "45 → 48" and "49" are totals including the 45 legacy cases; consistent across receipts.

## 6. Not done / scope

Did not run the round-42 C1 counter, the census selftest, or any C2 tool; no host mutation, no pacman, no installs (bash/find/git/python3 preexisting). One heavy counter (frozen C1 at tip) was run, twice sequentially (first direct print, then re-captured into the receipt file); no concurrent heavy runs. Scratch `/fast/scratch/hyaku/tsukuroi-r43/C1RevIntegration/` created and removed; receipts copied into the seat dir. Lane content untouched (read-only except this report and its receipt dir).
