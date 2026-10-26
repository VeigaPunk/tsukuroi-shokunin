VERDICT: supports

# C2-25 — C2 counter re-run, hashes, two lane revisions, scratch-clone fixture (seat C2ExecRerun)

Item: verify the shipped counter's sha256 against the pin and the freeze bytes; run
`tools/check-package-anatomy-r41.py` at the entry commit `9cc9aa77e30e0e23de2d4d2697b3b218ada02969`
and at lane tip `71851d636ab1bffaf8fee5016617c88878a666f1`; then, in a scratch clone at the tip, add
eight `VERDICT: holds` fixture files, commit them on `master` with the fixture identity, re-score, and
compare with pre-data control C2-K8. Every expected value in the item was reproduced exactly.

## 1. Counter bytes: shipped == pin == freeze

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum tools/check-package-anatomy-r41.py
c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f  tools/check-package-anatomy-r41.py
$ git show e479fdc54d0977ccd8112a42d8d139baaebcb02e:tools/check-package-anatomy-r41.py | sha256sum
c83e29a4f570422d5a975873460c4c5b061e33ac497b97d13c1383569ac1819f  -
$ git diff --stat e479fdc54d0977ccd8112a42d8d139baaebcb02e 71851d636ab1bffaf8fee5016617c88878a666f1 -- tools/check-package-anatomy-r41.py
(no output)
```

Both digests equal the declared `c83e29a4…1819f`, and the tool is byte-unchanged from the freeze commit
to the lane tip (no diff line). Lane tip's `refs/heads/master` and `refs/remotes/origin/master` both
resolve to `71851d63…` (`git rev-parse refs/remotes/origin/master`), so `_revision.bind` had both the
landed and pushed ancestry checks satisfied in both lane runs.

## 2. Lane runs (one counter process at a time)

Run A — entry commit, no `--repo` (tool defaults to the lane):

```
$ python3 tools/check-package-anatomy-r41.py --revision 9cc9aa77e30e0e23de2d4d2697b3b218ada02969
exit=1
revision=9cc9aa77e30e0e23de2d4d2697b3b218ada02969  branch_tip=71851d63…
entry_present=True rules_verified=8 verdicts_ok=0 host_ok=6 source_ok=1
duplicate_rows=0 duplicate_headings=0 novelty_base_hits=0 result=FAIL exit=1
```

Run B — lane tip:

```
$ python3 tools/check-package-anatomy-r41.py --revision 71851d636ab1bffaf8fee5016617c88878a666f1
exit=1
revision=71851d636ab1bffaf8fee5016617c88878a666f1  branch_tip=71851d63…
entry_present=True rules_verified=8 verdicts_ok=0 host_ok=6 source_ok=1
duplicate_rows=0 duplicate_headings=0 novelty_base_hits=0 result=FAIL exit=1
```

Both match the item's expectation (`rules_verified 8, host_ok 6, source_ok 1, verdicts_ok 0, FAIL`).
The verbatim JSON is in `w1/C2ExecRerun/rerun-9cc9aa77.json` (sha256 `032790b9…886b`) and
`w1/C2ExecRerun/rerun-71851d6-tip.json` (sha256 `faf931bb…0b48`); both stderr files are 0 bytes.
No rule carries a failure reason in either run (`rules_failed {}`), i.e. all eight rules verify and the
only missing predicate term is `verdicts_ok`, which is exactly the uncommitted reviewer verdicts:
at the tip neither `.ufo/waves/round-41/w1` nor `.ufo/waves/round-41/residual` exists
(`git ls-tree … 71851d63:.ufo/waves/round-41/w1` → `fatal: Not a valid object name`), and
`verdicts()` reads verdicts only from git objects at `<rev>` (tools/check-package-anatomy-r41.py:269-286),
so `verdicts_ok` is `0` by construction (tool:321).
The entry and `corpus/SOURCES.md` are byte-identical between the two revs
(`git diff --stat 9cc9aa77 71851d63 -- <entry> corpus/SOURCES.md` → no output).

Base state was read, not re-run (not part of this item): `before/c2-before.jsonl` records
`revision 0e5805a1…`, `tool_revision e479fdc5…`, `entry_present: false`, `result: "FAIL"`, `exit: 1`.

## 3. Scratch-clone fixture: eight `VERDICT: holds` files → PASS

Clone: `mktemp -d /fast/scratch/hyaku/tsukuroi-r41/C2ExecRerun/fx.XXXXXX` →

```
$ git clone -q --shared <lane> "$D" && git -C "$D" remote remove origin
$ git -C "$D" checkout -q -B master 71851d636ab1bffaf8fee5016617c88878a666f1
$ git -C "$D" rev-parse --show-toplevel          # == $D (checked before the commit)
$ git -C "$D" rev-parse --abbrev-ref HEAD        # master
```

Eight fixtures `.ufo/waves/round-41/w1/C2RevPA1.md … C2RevPA8.md`, each exactly:

```
VERDICT: holds
row PA<n>; C2ExecRerun scratch-clone fixture verdict
```

committed with `git -C "$D" -c user.name=fixture -c user.email=fixture@shokunin.local commit`:

```
40600b2046489792710725629548c8aee8cddcef fixture <fixture@shokunin.local> C2ExecRerun fixture: eight VERDICT: holds files
8 files changed, 16 insertions(+)
```

Score with the frozen lane tool against the clone:

```
$ python3 <lane>/tools/check-package-anatomy-r41.py --repo "$D" --revision 40600b2046489792710725629548c8aee8cddcef
exit=0
revision=40600b2046489792710725629548c8aee8cddcef branch_tip=40600b20…
entry_present=True rules_verified=8 verdicts_ok=8 host_ok=6 source_ok=1
duplicate_rows=0 duplicate_headings=0 novelty_base_hits=0 result=PASS exit=0
verdicts: PA1..PA8 each {holds:[".ufo/waves/round-41/w1/C2RevPA<n>.md"], fails:[], partly:[], malformed:[]}
```

PASS, as expected. Receipts: `w1/C2ExecRerun/fixture-holds-pass.json` (sha256 `324bf5c7…da97`, stderr
0 bytes), `fixture-sha256.txt` (the eight fixture digests), `fixture-commit.txt` (commit id, author,
stat, branch, clean status, exact invocation). Fixture texts are 2 lines each; the counter accepts a
verdict file only when the first line matches `VERDICT: (holds|partly|fails)` and the body names the row
id (tool:276-285), which the fixtures satisfy.

## 4. Comparison with pre-data control C2-K8

`w1-dispatch`-registered control, `controls/controls-c2.jsonl:9`:

| field | C2-K8 (rev `38035d92…`, recorded) | this rerun (rev `40600b20…`) |
|---|---|---|
| rules_verified | 8 | 8 |
| verdicts_ok | 8 | 8 |
| host_ok | 6 | 6 |
| source_ok | 1 | 1 |
| duplicate_rows / headings | 0 / 0 | 0 / 0 |
| novelty_base_hits | 0 | 0 |
| result / exit | PASS / 0 | PASS / 0 |

Identical on every predicate term. The variants differ only in what they commit: K8 committed the
candidate entry and `SOURCES.md` read from the lane worktree at freeze time plus the same shape of
verdict fixtures (`controls/run_controls.py:65,75`), whereas my clone commits only the eight verdict
files on top of the already-committed entry at `71851d63`. The entry was refined after that control ran
(`git diff --stat c7c40c0f 9cc9aa77 -- corpus/knowledge/alpm-package-anatomy-r41.md` → 3 insertions,
3 deletions), so the rerun also shows the refinement did not disturb `rules_verified`, `host_ok` or
`source_ok`: K8's PASS reproduces on the post-refinement entry, i.e. the counter is stable across both
entry states and the control's result is not an artifact of the pre-refinement text.

## 5. Extra discrimination (beyond the item's minimum)

- Committed, not worktree, is what counts: a second clone at the tip with the identical eight files
  written to the worktree but **not** committed scored `rules_verified 8, verdicts_ok 0, host_ok 6,
  source_ok 1, FAIL, exit 1` (`w1/C2ExecRerun/worktree-only-verdicts.json`, sha256 `faf931bb…0b48`,
  bit-identical to the tip run's output). So the six predicate terms other than `verdicts_ok` cannot be
  perturbed by an uncommitted working copy, and my PASS required the commit.
- `novelty_base_hits` is computed from the `BASE` commit via `git grep … BASE` (tool:259-262), not from
  the worktree, which is why both FAIL runs and the PASS run report `0` independently of the dirty lane
  worktree (`tools/check-self-assessment.py` modified, untracked `w1/` at the time of the runs).
- The lane was never mutated: no `git add/commit/checkout` in it (`git rev-parse HEAD` stayed
  `71851d63…`), all fixture writes/commits happened inside the two scratch clones under
  `/fast/scratch/hyaku/tsukuroi-r41/C2ExecRerun/`, and that scratch directory is removed.

## 6. Reading / caveat (no defect found)

The PASS I produced is a shape-gate result and nothing stronger: eight fabricated
`VERDICT: holds` files are sufficient, because the verdict dimension is provenance-blind. That is the
declared design ("the verdict files are the read, the lexical checks are shape gates"; tool:18-22) and
exactly what control C2-K8 exercises, so it is not a counter defect — but it means the item's expected
PASS does not validate any reviewer's findings. A real lane PASS still needs the eight genuine
`.ufo/waves/round-41/w1/C2RevPA<n>*.md` verdicts from the reviewer seats (in flight), whose content is
outside this item. Residual risk to record: if a later seat commits verdict files that merely name a row
and say `VERDICT: holds`, the counter cannot distinguish them from reviewed ones; only the reviewer
seats' own reports carry that judgment.

## 7. Receipts, environment, and what I did not do

Receipts (all in `.ufo/waves/round-41/w1/C2ExecRerun/`, text only, largest 4.7 KB):
`rerun-9cc9aa77.json/.err`, `rerun-71851d6-tip.json/.err`, `fixture-holds-pass.json/.err`,
`worktree-only-verdicts.json`, `fixture-sha256.txt`, `fixture-commit.txt`.
No tool was installed or upgraded (nothing needed; `python3` 3.14 from the host). No host mutation, no
pacman transaction, no service change, no lane write other than this report and the receipts above, no
scratch under `/tmp`. Four counter processes total (two lane runs, fixture run, worktree-only run), run
one at a time; the C2 counter is seconds, not the slow C1 selftest.

Observed, not caused by this seat: the lane worktree showed `corpus/knowledge/pacman-exec-environment-r40.md`
modified at 15:10 but not at 15:05 (before my first run it was absent from `git status --porcelain`).
No effect on this item: every read is a git object at an explicit revision, and novelty uses `BASE`.
The only other worktree modification (`tools/check-self-assessment.py`) predates the item.

Not done (out of item scope): did not run the C1 mount counter, did not run the census `--selftest`,
did not audit the actual reviewer verdict files' claims, did not re-run the base receipt (read from
`before/c2-before.jsonl` instead).
