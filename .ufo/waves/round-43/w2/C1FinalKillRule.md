VERDICT: supports

Seat C1FinalKillRule (item C1-F3), round 43 w2 (falsify), lane tsukuroi-shokunin.
Tip under test 8acf0b022586a0f3164c77659fb96ba5f90949b6, base 6951ead90566b2d74f7c45b4efca29246badad64.
All three kill-rule checks hold at the tip. No claim in the C1 frozen set is falsified by them.

Lane head at the time of the run (read-only):

    $ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse --verify 8acf0b022586a0f3164c77659fb96ba5f90949b6^{commit}
    8acf0b022586a0f3164c77659fb96ba5f90949b6
    $ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse --verify 6951ead90566b2d74f7c45b4efca29246badad64^{commit}
    6951ead90566b2d74f7c45b4efca29246badad64

Files extracted read-only with `git show <rev>:tools/boot-chain-audit.sh` into seat scratch:

    cd398e603cbd5894b74ca3c28740f2ab3379622a85fc62ac272259d45342930c  base-bca.sh   (6951ead, 1297 lines)
    77c80be827d69df08e172c531ddf87d6585c39140f6b3389b840b5d8ad9141ad  tip-bca.sh    (8acf0b0, 1322 lines)

---------------------------------------------------------------------------------------------------
KILL RULE (1) — per-function sha256, every top-level function, base vs tip
---------------------------------------------------------------------------------------------------

Method (receipts: `.ufo/waves/round-43/w2/C1FinalKillRule/fnhash.py`, `fnhash.out`,
`bca-base-to-tip.diff`). `fnhash.py` splits each script at column-0 `NAME()` starts; a block ends at
the first following line that is exactly `}` at column 0, and a one-line function
(`fixture_mode() { ...; }`, `fx_dir() { ...; }`, both at :205 and :207) is its own single line. The
block is hashed verbatim, boundary lines inclusive (byte-exact; no whitespace normalisation).

    $ python3 fnhash.py base-bca.sh tip-bca.sh
    # base funcs=33 tip funcs=34
    ...
    inputs_newer_than    NEW     tip_sha=04145e4f4f49812ba017f63c9376775fc27671134b993cfb2f8c36e7da07ff41  tip_lines=463-475
    boot_inputs_newer    CHANGED base_sha=4837c8e7d0496dc62467de6723e1a3e1e04084722980538eb8fbaa7c08c6d3f6
                                 tip_sha=4a426b918ca2701c5915893ac982ae146cffeccf007368133fdfe88867367354  lines 463-488 -> 477-497
    run_selftest         CHANGED base_sha=ce8ed80ede648c762259500cb11072162b2dd5cd478e791f750eae874f65fa71
                                 tip_sha=66956c0463d7b3c9f1474d04a0cd382c3fcb6bc7cccd013dfaeb2c71d5dd71fb  lines 876-1222 -> 885-1247
    # CHANGED SET: inputs_newer_than(NEW), boot_inputs_newer(CHANGED), run_selftest(CHANGED)
    # OUTSIDE ALLOWLIST: (none)
    # KILL-RULE-1: PASS

Changed-function set is exactly `{inputs_newer_than (new), boot_inputs_newer, run_selftest}` — the
allowlist. The remaining 30 functions are byte-identical between the two revisions; their full
per-function digests are in `fnhash.out` (e.g. `audit` f404ff57…65bd7 lines 647-807 -> 656-816,
`parse_limine_conf` a4535816…c961 lines 532-611 -> 541-620, `main` 3506705c…69c2 lines 1226-1295 ->
1251-1320; content identical, line offsets shifted only by the inserted function and the new cases).

Independent cross-check with bash's own parser (receipts `decl-base.txt`, `decl-tip.txt`): each script
was copied without its final `main "$@"` line, sourced in a throwaway `bash -c`, and `declare -f`
dumped for every function name from `declare -F`:

    base names 33 tip names 34
    added ['inputs_newer_than']
    removed []
    changed ['boot_inputs_newer', 'run_selftest']
    KILL-RULE-1 (declare-f normalised): PASS

Both parsers agree on the set, so the result does not depend on my splitter's heuristics. (Note:
`declare -f` strips comments, so this path alone would miss comment-only drift; the line-block
hashes above are comment-inclusive and show no such drift either.)

Non-function region: after removing every function block from both files, the residue differs by
exactly one blank line and nothing else —

    $ diff -u base-nonfunc.txt tip-nonfunc.txt
    @@ -179,6 +179,7 @@
    +
    (one added blank line; no executable top-level statement, default, or header text changed)

Whole-file diff is 3 hunks only (`bca-base-to-tip.diff`, 63 lines): the new `inputs_newer_than`
(tip :463-475), `boot_inputs_newer`'s body switching from `find … -print -quit | grep -q .` to
`inputs_newer_than "$btime" …` (tip :494-496), and the four `R43-C1-*` cases inside `run_selftest`
(tip :1225-1240).

Selftest-case delta (structural, from the text of `run_selftest`; receipts `base-cases.txt`,
`tip-cases.txt`, `LC_ALL=C comm`):

    45 base cases -> 49 tip cases
    removed cases: (none)
    added cases:   R43-C1-all-present-deep-newer
                   R43-C1-missing-start-point-deep-newer
                   R43-C1-missing-start-point-none-newer
                   R43-C1-missing-start-point-silent

45 -> 49 matches the frozen claim, and no pre-existing case was deleted.

---------------------------------------------------------------------------------------------------
KILL RULE (2) — round-42 C1 counter at the tip (expect PASS)
---------------------------------------------------------------------------------------------------

    $ python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/run-receipt.py \
        --revision 8acf0b022586a0f3164c77659fb96ba5f90949b6 \
        --tool-revision 8acf0b022586a0f3164c77659fb96ba5f90949b6 \
        --out .../.ufo/waves/round-43/w2/C1FinalKillRule/r42-c1-8acf0b0.jsonl \
        -- tools/score-size-invariance-r42.py --revision '{rev}' \
           --scratch /fast/scratch/hyaku/tsukuroi-r43/C1FinalKillRule/s
    {"out": ".../r42-c1-8acf0b0.jsonl", "revision": "8acf0b02…49b6",
     "tool": "tools/score-size-invariance-r42.py", "exit_code": 0}
    real 0m53.5s

Receipt (.ufo/waves/round-43/w2/C1FinalKillRule/r42-c1-8acf0b0.jsonl, 3 lines), parsed:

    header: receipt 1, revision 8acf0b022586a0f3164c77659fb96ba5f90949b6,
            tool_revision 8acf0b022586a0f3164c77659fb96ba5f90949b6,
            tool tools/score-size-invariance-r42.py, started_utc 2026-10-26T22:53:47Z, tool_sha256 c511104a…3e03
    body:   verdict "PASS", cases 10, invariant 10, ns_invariant 3, default_equal 1,
            non_invariant [], selftest_pass 1, selftest_rc 0,
            selftest_label "PASS (132 cases, 132 passed, 0 failed)",
            predicate "cases == 10 and invariant == 10 and ns_invariant == 3 and
                       selftest_pass == 1 and default_equal == 1"
    footer: receipt_end 1, exit_code 0, timed_out false, stderr_tail ""

Expected PASS, observed PASS, all five conjuncts at their required value.

Supporting fact for "no regression": the counter itself is untouched by this wave —

    tools/score-size-invariance-r42.py  base blob bf7c16bdba29fe972848c1cc853248b0e62bb132 == tip blob (same)
    tools/run-receipt.py                base blob 9944bd1899d3b4d3e55b0eeb7d12cddacbf6b9db == tip blob (same)

---------------------------------------------------------------------------------------------------
KILL RULE (3) — census selftest at the tip + census.sh unchanged
---------------------------------------------------------------------------------------------------

Census extracted at the tip and run from scratch with `TMPDIR` inside the seat scratch dir
(receipt `census-tip.sh`, sha256 7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9):

    $ bash census-tip.sh --selftest > census-selftest-tip.out 2> census-selftest-tip.err; echo rc=$?
    ...
    PASS cli: --help prints usage and exits 0 (S10-2) (exit 0)
    TSUKUROI_CENSUS_SELFTEST: PASS (132 cases, 132 passed, 0 failed)
    rc=0        (31.3s wall; stderr empty)

Observed label is exactly the expected `PASS (132 cases, 132 passed, 0 failed)`; exit 0.
Full transcript: `.ufo/waves/round-43/w2/C1FinalKillRule/census-selftest-tip.out` (135 lines).

`tools/tsukuroi-census.sh` is unchanged across the wave:

    $ git -C …/tsukuroi-shokunin diff --quiet 6951ead90566b2d74f7c45b4efca29246badad64 \
          8acf0b022586a0f3164c77659fb96ba5f90949b6 -- tools/tsukuroi-census.sh
    diff-quiet-rc=0
    blobs: base 18a1db6448358d7ecf4634570fcd2bf075eccb1b == tip 18a1db64…b1b
    working-tree extraction sha256 7c9f7903…77f9 at both revisions (`git show 6951ead:… | sha256sum` identical)

So the census cannot have regressed: the file the selftest ran at the tip is byte-identical to the
base file, and it passes 132/132.

---------------------------------------------------------------------------------------------------
Scope, host guard, and what I did not do
---------------------------------------------------------------------------------------------------

- Wrote only `.ufo/waves/round-43/w2/C1FinalKillRule.md` and
  `.ufo/waves/round-43/w2/C1FinalKillRule/` (12 receipts + `EVIDENCE.sha256` = 13 files, 416K total). No tracked
  lane file created, edited or deleted; no git/jj mutation in the lane (only `rev-parse`, `show`,
  `diff --quiet`, `rev-parse <rev>:<path>`); no writes to the fleet repo, sibling lanes, `~/.local/bin`
  or any PATH dir; no sudo, no package or service change, no host mutation, no btrfs ioctl.
- All scratch under /fast/scratch/hyaku/tsukuroi-r43/C1FinalKillRule (run-receipt also used
  /fast/scratch/hyaku for its sandbox clone); `TMPDIR` pointed there for the census run. After the
  census run no `tsukuroi-r3-2-selftest.*` directory remained under that `TMPDIR` (the selftest
  removed its own mktemp tree) and `s/` (the r42 counter's `--scratch`) was left empty — no residue
  outside the seat scratch. Scratch dir removed at the end
  (verified: `ls /fast/scratch/hyaku/tsukuroi-r43/C1FinalKillRule` → No such file or directory).
- No tools installed or upgraded; none needed. Versions used: bash 5.3.20, python 3.14.8,
  git 2.56.0.
- Did NOT run `tools/score-bootinputs-r43.py` (the frozen r43 counter) or
  `bash tools/boot-chain-audit.sh --selftest` myself: both are other seats' items in this wave, and
  the heavy-counter budget is one at a time. The 45 -> 49 selftest growth is therefore reported from
  the case text, not from an execution of the r43 selftest. The 132-case census label I do report is
  an execution (twice: inside the r42 receipt and standalone above).
- One measurement caveat, recorded rather than interpreted: the r42 receipt's `ns_cases` string shows
  the PLANE arm reading `BLOCKED (… Permission denied …)` under the receipt's fixed
  `PATH=/usr/bin:/bin` environment; that is the counter's own sandbox condition, the `verdict`
  predicate does not depend on it, and it is unchanged from the base behaviour (counter blob
  identical), so it is not a wave-w2 regression.

Evidence index: `.ufo/waves/round-43/w2/C1FinalKillRule/EVIDENCE.sha256`.
