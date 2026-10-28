VERDICT: supports

# C1-X9 — round-46 identity counter at FREEZE (mechanics only)

Scope: does the frozen round-46 C1 counter still work against the round-48 census bytes, and are its
selftest-derived legs consistent with 166 cases. This does **not** re-admit round-46 C1; that admission stays
withdrawn (see §5). Nothing in the lane was edited; all work ran under
`/fast/scratch/hyaku/tsukuroi-r48/TExecIdentity` (removed at the end; receipts copied first).

## 1. Frozen inputs (bytes under test)

| Object | Value | Evidence |
|---|---|---|
| Counter | `tools/score-census-identity-r46.py` sha256 `7c406eb5f4ba1f6265649f7102e7376882483180c161a66abc68e08cad9524ba` | `git -C … show ae99f021…:tools/score-census-identity-r46.py \| sha256sum`; byte-identical to the round-46 freeze `72cc2609` and to the working-tree copy → no counter drift |
| Census | `tools/tsukuroi-census.sh` sha256 `375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`, 216047 bytes, 3718 lines | `git -C … show ae99f021…:tools/tsukuroi-census.sh \| sha256sum`; equals the C1 frozen blob in the declaration |
| Counter CLI | `--revision` (required), `--scratch` (required, no `/tmp` fallback), `--lane` (default: counter's repo) | `counter-frozen.py:116-118` — matches the flag shape in my item, no adaptation needed |
| Predicate | `identity_ok == 1 and tracks_ok == 1 and symlink_ok == 1 and unverifiable_ok == 1 and cli_ok == 1 and nowrite_ok == 1 and selftest_pass == 1 and selftest_r46 >= 4` | `counter-frozen.py:66-67`, `:235` |

## 2. Run

```
cd /fast/scratch/hyaku/tsukuroi-r48/TExecIdentity
TMPDIR=/fast/scratch/hyaku/tsukuroi-r48/TExecIdentity \
  python3 <lane>/tools/score-census-identity-r46.py \
    --revision ae99f021b76f8eb1c8805d32d80644464afb1ff6 --scratch s
```

Exit **0**, empty stderr, wall 40.10 s (the item's 3-6 min estimate is on the high side: this counter runs one
selftest, not the C1 counter's four TMPDIR variants). Receipt: `TExecIdentity/r46-identity-ae99f02.jsonl`
(`"verdict": "PASS"`, `census_sha256 = 375aa737…e2426`). The counter wrote only beneath `--scratch` and removed
its own `r46c1-*` subtree (only the empty `s` directory remained).

## 3. Every leg

| Leg | Value | Observed |
|---|---|---|
| `identity_ok` | 1 | `bash F --identity`, rc 0, empty stderr, one line: `TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=375aa737…e2426 md5=d8080bd0…1d5c9 bytes=216047 lines=3718 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes` — digests/bytes/lines equal the counter's own computation over F; version = source literal `VERSION='census-v2'` (`census-frozen.sh:455`); planes = rollup key order (`:3708`) |
| `tracks_ok` | 1 | `G = F + "\n# r46 identity probe\n"` → `sha256=6df6ee93…aebd md5=e8704e75…faaf bytes=216069 lines=3720 … verified=yes`; all four fields differ from F → no constant writer |
| `symlink_ok` | 1 | symlink `S→F` → F's exact values, `verified=yes` |
| `unverifiable_ok` | 1 | all three cases rc 0, `sha256=unverifiable md5=unverifiable bytes=unverifiable lines=unverifiable … verified=no`, static fields (`version`/`planes`/`exit_map`) as in `identity_ok`: (a) `bash -s -- --identity < F` in a cwd holding decoy `bash` + decoy `tsukuroi-census.sh`; (b) `bash <(cat F) --identity`; (c) file replaced after open (`mv -f decoy R` on line 1) — this is the case that kills a path hasher, and it still holds after the round-48 `selftest_base_dir` rewrite |
| `cli_ok` | 1 | `[--identity --selftest]→2`, `[--identity --sample 3]→2`, `[--help]→0` with `--identity` named in usage, `[--bogus]→2` |
| `nowrite_ok` | 1 | cwd and TMPDIR snapshots (mode,size,mtime_ns) byte-identical before/after all identity runs and after the decoy runs |
| `selftest_pass` | 1 | rc 0, last line `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)` — full-matches the counter's `SELFTEST_RE` and the C1 claim's exact line |
| `selftest_r46` | 8 | `>= 4` required; 8 R46-C1 labels PASS, identical to the round-46 receipt's `selftest_r46 8` (`corpus/lessons/round-46-verifier-spotcheck.md:5` table, r46 `l1/c1-61e06740.jsonl`) |

## 4. Selftest-derived legs vs the 166-case claim

Consistent, no drift:

- The counter's own selftest leg reports exactly `166 cases, 166 passed, 0 failed` at the frozen census bytes
  (`r46-identity-ae99f02.jsonl`, `detail.selftest.last`); the counter's regex requires `0 failed`, so the 166/166/0
  triple is enforced, not merely observed.
- The 8 R46-C1 cases survive the round-46 → round-48 census rewrite (`census-frozen.sh:3478,3487,3493,3497,3505,3515,3517,3519`):
  self-line, appended-copy, symlink, stdin-decoy, replaced-after-open, parent-held-descriptor, plus the two
  `--identity` CLI rejections. The census grew 162 cases (round-46 measured revision `61e06740`) → 166 here, and the
  R46-C1 label count is unchanged at 8.
- Mechanism compatibility check: the round-48 `selftest_base_dir` alias band is 240-249 precisely because the
  R46-C1 held-descriptor case uses `exec 10<"$1"`; the source comment records the round-46 failure at an fd-10 alias
  (`census-frozen.sh:2068-2071`). Both that case and the counter's own stdin/replaced cases passed, so the alias
  choice does not collide with the R46-C1 descriptor fixture.
- The round-48 static guard cannot collide with this mechanism: `score-selftest-tmpdir-r48.py:144`
  `BASE_ASSIGN = re.compile(r'(?:^|[\s;])\w*base\w*=/tmp(?![\w/.-])')` matches a literal `…base…=/tmp` assignment, not
  `base=${TMPDIR:-/tmp}` (`census-frozen.sh:2072`), so the r46 identity/`selftest_base_dir` code does not trip it.

Additional measured leg (my own, sequential — no second selftest overlapped): the same frozen census run under a
**TMPDIR containing a space** (`…/TExecIdentity/dirty tmp`), `bash ./census.sh --selftest` → exit 0 in 61.0 s,
`TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)`, 8 `R46-C1` labels, 0 `FAIL`/`BAD` lines, empty
stderr, and the dirty TMPDIR left empty (fixture removed). Receipt: `TExecIdentity/selftest-dirty-tmpdir.txt`
(166 PASS lines, 15486 bytes). So the r46 identity mechanics also hold on the round-48 dirty-TMPDIR path, not only
on the counter's clean TMPDIR.

## 5. What this PASS does and does not mean

- It means only: the frozen round-46 counter is mechanically intact against the round-48 census bytes and does not
  regress the C1 mechanism it grades.
- It does **not** re-admit round-46 C1. That admission was withdrawn for a kill-rule reason
  (`corpus/lessons/round-46-verifier-spotcheck.md:171` "Admission: false", `:207-210` D1 `R46C-C1-KILL-RULE-FIRED`,
  capability admission "withdrawn until it re-verifies"). I did **not** run the r40 kill universe
  (`score-selftest-literals-r40.py`) or any predecessor counter at the freeze, so the r46 kill rule is
  **unmeasured by me** and remains the reason r46 C1 is not admitted.
- This run says nothing about C1's own four-TMPDIR/fail-fast/SIGTERM legs; those belong to the frozen r48 counter
  `tools/score-selftest-tmpdir-r48.py`, which I did not run (one selftest-budget, and another seat owns it).

## 6. Not done

- No r40 kill-universe / predecessor counter runs (explicitly outside this item; the freeze-time status of that
  clause stays unmeasured here).
- No run of `score-selftest-tmpdir-r48.py`; no `check-self-assessment.py`; no second concurrent selftest.
- No verification of the round-46 C2/depth counter.
- No tool installs were needed (python3, git, coreutils only).

Report paths (all under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-48/w2/`):
`TExecIdentity.md`, `TExecIdentity/r46-identity-ae99f02.jsonl`, `TExecIdentity/selftest-dirty-tmpdir.txt`,
`TExecIdentity/inputs.txt`.
