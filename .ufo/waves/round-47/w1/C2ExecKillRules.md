VERDICT: defect-found

Seat C2ExecKillRules, item C2-K4 (C2 kill rules at 77e9e2b2e96b85d8f048ae2087e246a542b71611).
The four assigned legs (a)-(d) all PASS as declared. The defect is in one *declared kill-rule
clause* of the C2 row, which the committed bytes contradict: verbatim "no committed tool writes
under a hardcoded /tmp" (SCORECARD.md:3066) is falsified by the R47-C2 fix itself, which adds a
literal `st_base=/tmp` write path (tools/tsukuroi-census.sh:2055-2058) and provably creates its
fixture tree under /tmp whenever TMPDIR holds a refused character. Details in F2; a reworded
clause is proposed at the end. Everything else in the kill rule holds byte-for-byte.

Read target: the census/boot-chain tools are byte-identical at the counted revision and in the
worktree, so these runs are runs of 77e9e2b2's bytes, not of a later edit:
  sha256(tools/tsukuroi-census.sh)          = adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41
  git show 77e9e2b2:tools/tsukuroi-census.sh | sha256sum = same line above (both hashes observed in one call)
  sha256(tools/boot-chain-audit.sh)         = 77c80be827d69df08e172c531ddf87d6585c39140f6b3389b840b5d8ad9141ad
  git show 77e9e2b2:tools/boot-chain-audit.sh | sha256sum = same line above
  base (91601905) census sha256            = ac4e38ff99df044bf17410722b253965402afa1556fd105dde181e19e048f48e
  HEAD is f6bc6d05; `git diff 77e9e2b2 HEAD -- tools/` is empty (only .ufo wave files and
  corpus/knowledge/adjacency-anchors-r19.json moved), so no tool bytes drifted after the freeze.
Receipts (all under .ufo/waves/round-47/w1/C2ExecKillRules/): selftest-final.txt,
selftest-space.txt, selftest-base-space.txt, selftest-base-free.txt, selftest-nodir.txt,
identity-final.txt, identity-base-file.txt, identity-base.txt, live-base.out, live-final.out,
live-base.stripped, live-final.stripped, diff-stripped.txt, diff-raw.txt, bootchain-final.txt,
bootchain-base.txt, bootchain-space.txt, r46-counter-impl.json, tmp-cleanup-evidence.txt.
Scratch (removed at the end): /fast/scratch/hyaku/tsukuroi-r47/C2ExecKillRules/.

=== (a) selftest, space-free TMPDIR: PASS 164/164, 8 (R46-C1), 2 (R47-C2) — PASS ===
Command (run from /fast/scratch/hyaku/tsukuroi-r47/C2ExecKillRules, TMPDIR=.../tmp, space-free):
  env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=/fast/scratch/hyaku/tsukuroi-r47/C2ExecKillRules/tmp \
    bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh --selftest
Observed: rc=0; stdout selftest-final.txt:167 =
  "TSUKUROI_CENSUS_SELFTEST: PASS (164 cases, 164 passed, 0 failed)"; stderr empty.
  grep -c 'R46-C1' selftest-final.txt -> 8   (labels at selftest-final.txt:157-164)
  grep -c 'R47-C2' selftest-final.txt -> 2   (labels at selftest-final.txt:165-166)
  The eight R46-C1 lines are the six id_check identity cases plus the two check_cli cases
  (selftest-final.txt:157-164), all "PASS ... (exit 0)" / "(exit 2)" as designed.
The declaration's own frozen counting command, i.e. under a TMPDIR that contains a space:
  S=/fast/scratch/.../spacetest; mkdir -p "$S/t 2";
  env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" bash .../tools/tsukuroi-census.sh --selftest
Observed: rc=0; selftest-space.txt last line "PASS (164 cases, 164 passed, 0 failed)";
  8 (R46-C1) and 2 (R47-C2) labels again. Matches the declared target "PASS 164/164 rc 0 under a
  space TMPDIR, and PASS 164/164 space-free" (SCORECARD.md:3066, target column).
Before-state reproduced from base bytes (census-base-run.sh = git show 91601905:tools/tsukuroi-census.sh):
  same space TMPDIR -> rc=1, "TSUKUROI_CENSUS_SELFTEST: FAIL (162 cases, 13 passed, 149 failed)",
  149 "^FAIL" lines (selftest-base-space.txt). This is exactly the declared before at base
  ("FAIL (162 cases, 13 passed, 149 failed) rc 1", SCORECARD.md:3066 before column).
  same base bytes, space-free TMPDIR -> rc=0 "PASS (162 cases, 162 passed, 0 failed)"
  (selftest-base-free.txt), so 164 = 162 + 2 new cases, as declared.
Cost observed: 26.8 s (space-free), 27.5 s (space), 30.4 s (base space) — one selftest at a time.

=== (b) --identity line shape: one line, frozen field order, verified=yes — PASS ===
Command: bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh --identity
Observed rc=0, empty stderr, exactly one non-empty line (identity-final.txt, grep -c . -> 1):
  TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41 md5=cf005e9a946e0a37c96f81d443d520d8 bytes=212252 lines=3644 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes
  Field order observed: version, sha256, md5, bytes, lines, planes, exit_map, verified — the order
  the item names. The sha256 field equals `sha256sum tools/tsukuroi-census.sh` and equals the
  77e9e2b2 blob hash, so the line names the bytes it executes. lines=3644 equals `wc -l` on the
  file; the same value the frozen round-46 counter reads (r46-counter-impl.json "want" block).
Shape unchanged from base: base census extracted to a regular file and run with --identity
  (identity-base-file.txt) prints the same token sequence with the same field order and the same
  planes/exit_map; sed 's/=[^ ]*/=/g' on both lines diffs empty ("SHAPE-IDENTICAL" observed).
  Base byte fields differ, as they must: sha256=ac4e38ff… bytes=210762 lines=3622.
  Run through process substitution (identity-base.txt) the base line reads
  sha256=unverifiable … verified=no, which is the designed stdin/pipe arm, not a shape change.

=== (c) live census, digits-stripped base vs final: byte-identical, rc identical — PASS ===
Commands (both from /fast/scratch/hyaku/tsukuroi-r47/C2ExecKillRules, method of seat C1ExecKillLive):
  env -i PATH=/usr/bin:/bin LC_ALL=C bash <(git -C <lane> show 916019057147d7e9ba6b137647b2cee26decf4b8:tools/tsukuroi-census.sh) > live-base.out 2> live-base.err
  env -i PATH=/usr/bin:/bin LC_ALL=C bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh                     > live-final.out 2> live-final.err
Observed: base rc=2, final rc=2 (same exit-map code: worst plane BLOCKED — packages
  "pacman -Qkk sample probe error: error: openai-chatgpt: missing required signature" and systemd
  "systemctl --user unusable rc=1"); both stderr files 0 bytes; both 13 lines / 7583 bytes.
  sed 's/[0-9]//g' on each, then diff -u -> empty; diff-stripped.txt is 0 lines (STRIPPED-IDENTICAL).
  Raw diff (diff-raw.txt, 12 lines) is (i) the header timestamp 08:56:18Z vs 08:56:27Z,
  (ii) C6_psi_full_total_us 100948104 vs 100968498, (iii) C6_avail_kb 22168364 vs 21662864 —
  three digit-only live values, no text/field/order change.
Exit map: census `case "$roll"` block is untouched by the round-47 diff (git diff
  91601905 77e9e2b2 -- tools/tsukuroi-census.sh shows exactly 4 hunks — @@ -408 comment,
  @@ -598 usage text, @@ -2045 run_selftest fixture base, @@ -3459 the two R47-C2 cases — none
  of them in a verdict, rollup or exit-code path); CLI parity observed: --help rc 0 both,
  --bogus rc 2 both, "--identity --selftest" rc 2 both; live rc 2 both.

=== (d) boot-chain-audit --selftest: PASS 49/49 — PASS ===
Command: bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/boot-chain-audit.sh --selftest
Observed: rc=0, "TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=49 failed=0" (bootchain-final.txt).
Base bytes give the same count (bootchain-base.txt: PASS total=49 failed=0), and the tool is
byte-identical at 77e9e2b2 and in the worktree (sha 77c80be8… both), so 49/49 is unchanged.
Also PASS 49/49 under a TMPDIR containing a space (bootchain-space.txt) — it honours
${TMPDIR:-/tmp} and never needed the whitespace guard.

=== Cross-check with the frozen round-46 counter (not my item, cheap corroboration) ===
python3 tools/score-census-identity-r46.py --revision 77e9e2b2 --scratch <scratch>/s46 ->
  verdict PASS; identity_ok 1, tracks_ok 1, symlink_ok 1, unverifiable_ok 1, cli_ok 1,
  nowrite_ok 1, selftest_pass 1, selftest_r46 8; selftest last line "PASS (164 cases, 164 passed,
  0 failed)"; 28.0 s (r46-counter-impl.json). So the "all (R46-C1) cases still pass" clause holds
  under the counter that owns it (predicate selftest_r46 >= 4).

=== Findings ===
F1 (calibration, wording): the kill rule says "all six `(R46-C1)` cases still pass"
  (SCORECARD.md:3066) but the selftest emits EIGHT PASS lines carrying `(R46-C1)` — six id_check
  identity cases plus two check_cli cases (selftest-final.txt:157-164) — and the count is 8 at
  base too (same eight labels in selftest-base-free.txt). 8 >= 6 so the clause is satisfied, but
  the number is wrong; the frozen r46 counter uses selftest_r46 >= 4 instead. Not a functional
  failure; it would mislead a reader diffing label counts.
F2 (kill-rule clause contradicted by the landed fix): the same clause set ends
  "no committed tool writes under a hardcoded /tmp" (SCORECARD.md:3066). The R47-C2 change adds a
  literal /tmp fallback, tools/tsukuroi-census.sh:2055-2058:
      local st_base=${TMPDIR:-/tmp}
      case "$st_base" in
        *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
      esac
      work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")
  and it fires in practice: strace of the space-TMPDIR selftest shows the fixture tree created at
  the hardcoded path —
      mkdir("/tmp/tsukuroi-r3-2-selftest.fIuF9A", 0700) = 0            (tmp-cleanup-evidence.txt)
  — while the caller asked for "$S/t 2". At base the only /tmp reference was the
  ${TMPDIR:-/tmp} default, which a caller's TMPDIR always overrode; the new line overrides a SET
  TMPDIR with a constant. So the clause as written does not hold of the bytes it grades. Two
  readings are possible and only the L1 can pick: (i) the clause is about a *fixed* /tmp path that
  ignores TMPDIR (then the sentence is too broad and should be reworded), or (ii) the clause
  forbids any /tmp write once TMPDIR is set (then the fix itself violates it). The write is
  otherwise well-formed: mode 0700, mktemp-random name (no symlink/pre-creation race), and the
  EXIT trap removes it — strace shows the top-level unlinkat ... AT_REMOVEDIR = 0
  (tmp-cleanup-evidence.txt), i.e. my run left nothing behind.
  Proposed replacement text for that clause (report text only):
      "no committed tool writes to a fixed /tmp path or ignores a usable TMPDIR; the census
       selftest falls back to /tmp only when TMPDIR holds a character the root-override locator
       refuses, under mktemp -d (mode 0700) with an EXIT-trap removal"
  Scope note: `git diff --name-only 91601905 77e9e2b2 -- tools/` lists just two paths —
  `tools/tsukuroi-census.sh` (edited, the 4 hunks above) and `tools/check-scrub-admission-r47.py`
  (new, C1's counter) — so the census is the round's only *edited* tool.
  tools/check-recheck-commands.py:1025 contains "/tmp/fp.txt", but only inside a quoted
  recheck-command string (present at base too); that tool writes nothing.
F3 (robustness edge, pre-existing): the derivation is charset-only. With
  TMPDIR=/fast/scratch/.../nope (classifiable but nonexistent) the selftest dies at mktemp:
  rc=1, stderr "mktemp: failed to create directory via template '.../nope/tsukuroi-r3-2-selftest.XXXXXX':
  No such file or directory", and NO "TSUKUROI_CENSUS_SELFTEST:" summary line is printed
  (selftest-nodir.txt). Base behaves the same way, so this is not a regression, but the declared
  "derives a classifiable fixture base" contract does not cover existence/writability: a caller
  TMPDIR that is set, clean and missing still yields a bare mktemp failure rather than the /tmp
  fallback. Suggested next-round seam: test -d/-w too, not only the character class.
F4 (observation, /tmp residue ownership): because of the F2 fallback every dirty-TMPDIR selftest
  run materialises a 0700 fixture tree in world-writable /tmp (1777 root:root, observed
  `stat -c '%a %U %G' /tmp` -> 1777 root root). During this wave several
  /tmp/tsukuroi-r3-2-selftest.* trees came and went (4T0v22 created 06:05:56, gone by 06:09:44;
  xcMSGK created 06:07:53, gone by 06:09:44; hmJSpA created 06:02:27, still present at 06:09:44) —
  the ~160 concurrent seats run the same command, and a run killed with SIGKILL leaves its tree
  (the EXIT trap cannot run). My own runs left none (strace evidence above; `ls -A clean1` empty
  after a space-free run). Attribution of a residual tree to a specific seat is not possible from
  here, so I removed none of them (a live peer may still own one). The predictable-prefix/race
  question itself is seat C2SentTmp's item; this note only records that the residue is real and
  that /tmp is the shared location.

=== Not done / limits ===
- No C1 scrub-admission legs, no counter mutations, no battery re-run: other seats own them.
- I did not verify the (R46-C1) count at base with the r46 counter (only its label count, above).
- I did not run any host mutation: no pacman, no systemctl start/stop, no sysfs write, no btrfs
  command; no `unshare`/mount was needed. No tool was installed or upgraded this seat (pacman is
  paused host-wide; nothing was missing).
- The exit-code leg was checked at four CLI points plus the live run; a full 0/1/2 verdict sweep
  (HEALTHY path) is only exercised by the selftest's fixture cases (space-free PASS 164/164),
  which is the coverage the declaration cites.
