VERDICT: supports

Item G-4 — C1 and C2 are causally separable. In a scratch clone, revision A (declaration + only the
C1 change) passes the C1 counter and fails the C2 counter; revision B (declaration + only the C2
change) passes the C2 counter and fails the C1 counter. All four runs ended in a scored counter
verdict (exit 0/1), never a binding refusal (exit 2). Counters used at the lane tip equal the frozen
ones: `sha256sum tools/score-selftest-literals-r40.py tools/check-exec-environment-r40.py` →
`8b06de18…f2f0159` and `d4a2bb94…ebb7d9d` (declared values), and
`git diff --stat a447b67..f951f288 -- tools/score-selftest-literals-r40.py tools/check-exec-environment-r40.py tools/_revision.py`
is empty.

# 1. Fixture: scratch clone, two revisions

    S=/fast/scratch/hyaku/tsukuroi-r40/CritSeparability        # export TMPDIR="$S/tmp"
    D=$(mktemp -d "$S/fx.XXXXXX")
    git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D"
    git -C "$D" remote remove origin
    git -C "$D" rev-parse --show-toplevel      # → $D   (TOPLEVEL_OK, checked before any commit)
    git -C "$D" config user.name fixture; git -C "$D" config user.email fixture@shokunin.local
    # A: declaration + only C1
    git -C "$D" reset --hard 758a4b08c6ea259a033f071fc864b544511fb172 -q
    git -C "$D" cherry-pick -x c707e356c2911646f7304d706eb77d118e510610
    A=$(git -C "$D" rev-parse HEAD)      # 50aca38c9be9548ef397643cf30ea273bb793163
    # B: declaration + only C2
    git -C "$D" reset --hard 758a4b08c6ea259a033f071fc864b544511fb172 -q
    git -C "$D" cherry-pick -x bf2380503b8e4a5d33162026854b0b7b66d18b86
    B=$(git -C "$D" rev-parse HEAD)      # 948b2e36201c893f2313b01c2f2313964ed3fa74

Both cherry-picks applied cleanly (C1's parent is the declaration; C2's parent is C1, but C2 touches
no path C1 touches). Tree-level confirmation that each revision carries exactly one claim's change:

    git -C "$D" diff --stat "$A" c707e356c2911646f7304d706eb77d118e510610   # → empty (A tree ≡ C1 commit tree)
    git -C "$D" diff --stat 758a4b08 "$A"   # → tools/tsukuroi-census.sh | 36 ++++++++++
    git -C "$D" diff --stat 758a4b08 "$B"   # → corpus/SOURCES.md | 7 ++++
                                            #   corpus/knowledge/pacman-exec-environment-r40.md | 45 +++++
    git -C "$D" diff --stat "$B" bf2380503b8e4a5d33162026854b0b7b66d18b86
                                            # → tools/tsukuroi-census.sh | 36 +++ (B is the C2 commit minus C1's census hunk)

The two commits' path sets are disjoint (`git show --name-only c707e35` → `tools/tsukuroi-census.sh`;
`git show --name-only bf23805` → `corpus/SOURCES.md`, `corpus/knowledge/pacman-exec-environment-r40.md`),
so separation by construction is expected; the runs below test that the counters respect it.

The revision binder (`tools/_revision.py` check 5) requires the revision under test to be an ancestor
of `--branch`, so `master` in the clone was pointed at A for the A runs and at B for the B runs
(`git -C "$D" reset --hard "$A" -q` before the A pair, `… "$B" -q` before the B pair). `origin` was
removed so check 6 cannot fire.

# 2. Results (the 2×2 the item asks for)

    cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
    # C1 on A (master=A)
    python3 tools/score-selftest-literals-r40.py --repo "$D" --revision "$A" --scratch "$S/c1-A" --jobs 2
    # C2 on A (master=A)
    python3 tools/check-exec-environment-r40.py --repo "$D" --revision "$A"
    # C2 on B (master=B)
    python3 tools/check-exec-environment-r40.py --repo "$D" --revision "$B"
    # C1 on B (master=B)
    python3 tools/score-selftest-literals-r40.py --repo "$D" --revision "$B" --scratch "$S/c1-B" --jobs 2

| counter | revision | exit | `result` | decisive fields | receipt |
|---|---|---|---|---|---|
| C1 `score-selftest-literals-r40` | A `50aca38` (C1 only) | **0** | **PASS** | `baseline_pass 1` (124 cases), `neutral_pass 3`, `mutants_applied 9`, `survivors 0`, `selfref 5` | `CritSeparability/c1-on-A.json` |
| C2 `check-exec-environment-r40` | A `50aca38` (C1 only) | **1** | **FAIL** | `entry_present false`, `rules_verified 0`, `source_ok 0`, `counts_ok 0`, `novelty_base_hits 0` | `CritSeparability/c2-on-A.json` |
| C2 `check-exec-environment-r40` | B `948b2e3` (C2 only) | **0** | **PASS** | `rules_verified 8`, `duplicate_rows 0`, `duplicate_headings 0`, `source_ok 1`, `counts_ok 2`, `novelty_base_hits 0` | `CritSeparability/c2-on-B.json` |
| C1 `score-selftest-literals-r40` | B `948b2e3` (C2 only) | **1** | **FAIL** | `baseline_pass 1` (119 cases), `neutral_pass 3`, `mutants_applied 9`, `survivors 9` (M1–M9 all), `selfref 5` | `CritSeparability/c1-on-B.json` |

Expected pattern (C1 PASS on A, C1 FAIL on B, C2 PASS on B, C2 FAIL on A) holds exactly. Wall times:
C1 runs ≈200 s and ≈241 s with `--jobs 2`; C2 runs ≈2 s.

Both FAILs are scored failures, not binding refusals: the refusal path returns exit 2 with
`{"counter": …, "error": "E-…", "exit": 2}` — see `c2-on-A-clonetool.json`'s sibling attempt below. Each
FAIL record above carries the full counter body (`derived`, `host`, `novelty`, `mutants`, `neutrals`),
i.e. the counter evaluated its inputs. Transparency about one discarded attempt: the first C2-on-A run
returned `{"error": "E-REVISION-NOT-LANDED refs/heads/master: 50aca38c9be9 is not an ancestor", "exit": 2}`
because `master` then sat at B; it was rerun with `master=A` and returned the exit-1 FAIL above.

# 3. Independence evidence (why the pattern is causal, not incidental)

1. **The counters share no input.** `grep -n "SOURCES\|corpus\|knowledge" tools/score-selftest-literals-r40.py`
   → no match (C1 reads only `tools/tsukuroi-census.sh` at the revision, `CENSUS` at line 51, and runs
   its copy in scratch with `cwd=/`). `grep -n "census\|selftest" tools/check-exec-environment-r40.py`
   → no match (C2 reads only the entry, `corpus/SOURCES.md` and the hash-pinned frozen snapshots).
2. **C2's revision-scoped reads are `git show`**, not the worktree: `git_show(a.repo, b.sha, ENTRY)` and
   `git_show(a.repo, b.sha, SOURCES)` at `tools/check-exec-environment-r40.py:249-251`.
3. **The declaration changes neither claim's surface.** Census blob ids: base `53b294a` → `e2494db`,
   declaration `758a4b0` → `e2494db`, B → `e2494db` (identical); A → `16438ee` (C1's blob). So C1's FAIL
   on B is exactly the pre-commit census state, and C1's PASS on A is caused solely by `c707e35`. The
   case-count delta 119 → 124 is the five declared mount-table fixtures.
4. **C2 is absent at A, not merely unquoted.** `git -C "$D" cat-file -e "$A":corpus/knowledge/pacman-exec-environment-r40.md`
   → `fatal: path … exists on disk, but not in '50aca38…'`; `git -C "$D" show "$A":corpus/SOURCES.md | grep -c '^| S2\(19\|2[0-5]\)'`
   → `0`.
5. **The frozen inputs C2 verifies against exist at the declaration**, so A and B differ only by the
   claim deltas: `git ls-tree --name-only 758a4b0 .ufo/waves/round-40/frozen/src/` lists the 8 pinned
   files (`added at a447b67`, `git log --diff-filter=A -- .ufo/waves/round-40/frozen/src/SHA256SUMS`).

# 4. Confound tested: C2 borrows its frozen inputs from its own tree

`SRC_DIR = TOOL_ROOT / '.ufo/waves/round-40/frozen/src'` and `CAP_DIR = …/hostcap` (`check-exec-environment-r40.py:65-66`,
`TOOL_ROOT = Path(__file__).resolve().parent.parent`), so a lane-tool run reads the lane's frozen dir
regardless of `--repo`. If the verdict depended on that borrowed state, the clone experiment would not
be self-contained. Rerun with the clone's own copy of the counter at both revisions:

    python3 "$D/tools/check-exec-environment-r40.py" --repo "$D" --revision "$B"   # exit 0, PASS,
        # rules_verified 8, source_ok 1, counts_ok 2, novelty_base_hits 0   (c2-on-B-clonetool.json)
    python3 "$D/tools/check-exec-environment-r40.py" --repo "$D" --revision "$A"   # exit 1, FAIL,
        # entry_present false, rules_verified 0                            (c2-on-A-clonetool.json)

Identical verdicts and identical counts from both tool trees. The borrowing is therefore immaterial
for G-4 (the pinned dirs are byte-identical in the clone and the lane at every revision used); it is a
property of the frozen counter, not a coupling between C1 and C2.

# 5. Counterexamples that would have falsified separability, and did not

- *C1 passing at B through some shared mechanism* (self-reading selftest, corpus-dependent fixture,
  or a mutant killed by text rather than behaviour): refuted — C1 on B shows `selfref 5` (unchanged),
  `mutants_applied 9`, `survivors 9`, with `baseline_pass 1`; the census at B is byte-identical to the
  base census, and no C1 input comes from `corpus/`.
- *C2 passing at A* through tolerating a missing entry, or through an entry reachable from the frozen
  tree or the base registry: refuted — `entry_present false`, `rules_verified 0`, `source_ok 0`,
  `novelty_base_hits 0`, exit 1, from both the lane tool and the clone tool.
- *Either FAIL being a could-not-evaluate*: refuted — exit 1 with a full scored record in every case;
  the only exit-2 record produced during the seat (`c2-on-A.json` first attempt,
  `E-REVISION-NOT-LANDED`) was caused by the clone's `master` pointer and was rerun away.

# 6. No-harm

- Lane untouched: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD` → `f951f288483c1af0cef4afd458488b84cf7a2165`
  (dispatch tip), `git diff --cached --stat` empty, `git status --porcelain` shows only the pre-existing
  dirty set (`make-w1-spec.py`, `revs.json`, `w1-dispatch.*`, `w1.ready*`, `w1/`, `corpus/lessons/round-40.md`)
  plus this seat's own report/receipts. No commit, checkout, reset, stash or jj command ran in the lane;
  all committing happened in `$D` under `/fast/scratch/hyaku/tsukuroi-r40/CritSeparability/` with the
  fixture identity.
- Reads only, no host mutation: no pacman transaction, no service action, no sudo, no mount outside
  `unshare`, no signal to any process not started by this seat. Nothing was installed or upgraded.
- Scratch removed after the receipts were copied into `.ufo/waves/round-40/w1/CritSeparability/`
  (`rm -rf -- /fast/scratch/hyaku/tsukuroi-r40/CritSeparability`); no `/tmp` path is used as evidence.

# 7. Residual notes (not defects against G-4)

- The C2 counter answers "does the entry at `<REV>` satisfy the rule-cell predicate", not "is the entry
  true"; falsity of EX1–EX8 is outside this item and belongs to the C2 attack seats.
- C1's PASS on A rests on the census selftest's self-containment: the copy ran from scratch with
  `cwd=/`, `HOME` inside scratch, `TMPDIR` inside scratch, so repo state could not have contributed;
  if a future census revision reads its own tree, that assumption must be re-tested.
- Both C1 runs were made with `--jobs 2` as instructed, not the counter default of 4.
