VERDICT: falsifies

# R49ConnWave — cross-lane counter pattern scan (item F-3)

Scope: how sibling lanes freeze counters and bind seat verdicts; whether any sibling defect
pattern is also present in this lane's C1/C2/C3 counters, tested against the freeze bytes
`55c07cd3f8bff2e12117c34d57b4c618de74d85c`. Read-only throughout: no file in
tsukuroi-shokunin or any sibling lane was created, modified or deleted; every fixture lives
under `/fast/scratch/hyaku/tsukuroi-r49/R49ConnWave/` and is removed below.

## 0. Bounds actually used (the item's globs are empty)

The item's literal read set `ls -t <lane>/tools/*.py` yields **zero files for all three
siblings**:

```
$ ls -t /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/*.py \
        /home/vgpnk/Projects/shokunin/kumitate-shokunin/tools/*.py \
        /home/vgpnk/Projects/shokunin/kake-shokunin/tools/*.py
ls: cannot access '.../kaidoku-shokunin/tools/*.py': No such file or directory
ls: cannot access '.../kumitate-shokunin/tools/*.py': No such file or directory
ls: cannot access '.../kake-shokunin/tools/*.py': No such file or directory
```

`kumitate-shokunin` and `kake-shokunin` have no `tools/` directory at all (they use
`scripts/`); `kaidoku-shokunin/tools/` exists but contains only `round-25/` … `round-46/`
subdirectories — the Python instruments sit one level down
(`kaidoku-shokunin/tools/round-25/ruler.py`, …). I substituted the nearest populated set so
the scan still answers the question, capped at six tool files, newest first:

| file | role |
|---|---|
| `kake-shokunin/scripts/append_guard.py` | append-only correction guard over committed blobs |
| `kake-shokunin/scripts/landed_check.py` | report-cited commit vs branch ancestry |
| `kake-shokunin/scripts/citation_lint.py` | commit-citation hygiene over frozen population |
| `kake-shokunin/scripts/header_audit.py` | offline manifest audit |
| `kake-shokunin/scripts/quote_class.py` | derived (never asserted) quote-match class |
| `kaidoku-shokunin/.ufo/gates/c1-census-v10.py` | re-key discipline (E22 disposition) |

Reports: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-48/tsukuroi.md` (newest overall,
09:55 today) and `round-48/kengaku.md` (newest sibling, 2026-10-27 09:24).

## 1. (a) One freezing/binding idea worth copying, with path:line

**`kake-shokunin/scripts/append_guard.py` — the counter carries its own adversarial
environment case, so the read discipline cannot silently regress.**

- `append_guard.py:30` — the declared rule: "Committed bytes only: every read goes through
  `git ls-tree` / `git cat-file`; the worktree is never touched and inherited `GIT_*`
  variables are scrubbed."
- `append_guard.py:53-57` — the implementation, a deletion of every `GIT_*` name from a copy
  of the environment before any child `git` runs:
  `def _env() -> dict: … for k in [k for k in env if k.startswith("GIT_"): del env[k]`.
- `append_guard.py:531-532` — the non-obvious half: a selftest case whose *expected result is
  unchanged* under a hostile environment —
  `case("X12_git_env_scrubbed", 0, [], argv="same_commit", env={"GIT_DIR": "/nonexistent-selftest-dir"})`.

The idea is not "scrub the environment" (this lane already owns that helper); it is that the
hardening is **proved inside the counter's own selftest by a case that passes only because the
scrub happened**. A negative case in the tool, not a claim in the docstring.

Secondary, for seat binding: `landed_check.py:2` resolves every hex token a report cites to a
git object and checks branch ancestry. This lane's C1 `report_citations_ok`
(`tools/check-scrub-admission-r49.py:244`) resolves seat-report `file:line` citations
against pinned snapshot line counts but never checks that a cited *commit* is an ancestor of
the lane branch.

## 2. (b) Sibling defect pattern, tested against the freeze bytes — and it is present

**Pattern: a claim scored on bytes that are not the frozen bytes.** kengaku round 48 states
it twice in its own words — "Neither verifies at a committed landing tip; neither is admitted"
(`.ufo/reports/round-48/kengaku.md:5`) and "Stage-2 freeze absent, so command was not run on
the final lane tip" (`:29`, `:30`).

This lane's C2 has the same defect, measurably, at the freeze revision. Frozen counter,
frozen bytes, real lane, read-only, `TMPDIR` inside scratch:

```
$ python3 <freeze>/tools/check-adjacency-table-r49.py --revision 55c07cd… --lane <lane>
{"adj_rows": 7, "linked_rows": 7, "bare_ranges": 0, "anchors_ok": 7, "registry_ok": 7,
 "anchors_checker_rc": 1, "problems": ["tools/check-adjacency-anchors.py rc=1: …"],
 "verdict": "FAIL"}

$ python3 <freeze>/tools/check-adjacency-table-r49.py --revision 32a85560… --lane <lane>
{"adj_rows": 7, "linked_rows": 7, "bare_ranges": 0, "anchors_ok": 7, "registry_ok": 7,
 "anchors_checker_rc": 0, "verdict": "PASS"}
```

Cause, located to the byte. `32a85560` is **not** the freeze: it is the commit *after* it
(`git merge-base --is-ancestor 55c07cd 32a85560` → true), subject "round-49: w1 spec +
validated dispatch (73 seats, policy v2); IN-109 repin 2642->2660". At the freeze revision:

| object | value at `55c07cd` | value at `32a85560` |
|---|---|---|
| `corpus/knowledge/adjacency-anchors-r19.json` IN-109 `found_line` | `2642` | `2660` |
| `tools/tsukuroi-census.sh:2642` | `'^PLANE systemd: DEGRADED .*timer_fail=0 timer_unknown=1'` | — |
| `tools/tsukuroi-census.sh:2660` | `check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED` | — |

The census row's own quote is 18 lines below the line the registry asserts, so the committed
sub-checker emits
`INBOUND-CLASSIFICATION-WRONG … adjacency-anchors-r19.json:inbound[108]` and exits 1. The
predicate leg `anchors_checker_rc == 0` is therefore **false at the freeze**.

**C2 as frozen does not hold.** All five content legs (7/7/0/7/7) are green at the freeze; the
single borrowed leg is red because a registry row was left stale in the freeze commit and
repinned afterwards. This is a recurring row: the round-48 report records the previous repin
of the same row — "`d7843b3a…` — IN-109 anchor repin 2593→2642"
(`.ufo/reports/round-48/tsukuroi.md:20`). Round 48 sequenced that repin so the claim was scored
on green bytes; round 49 did not.

Why the pre-data control did not catch it: `controls/battery.py:19` is
`REV = os.environ.get('BATTERY_REV', FREEZE)`, and the K-pass receipt's own `revision` field
reads `32a855608aa3ebb19b0602a94cc33bcfda564a61`
(`controls/battery-summary-r49-c2.jsonl`, control `K-pass`, `_rc 0`, `anchors_checker_rc 0`).
L1 discloses the substitution honestly — `frozen/FROZEN.md:62`, "## Control outcomes (scored
at `32a85560`, before wave w1 was dispatched)", and "The K-pass fixtures prove each counter
can pass; they are not the claim measurement" — but the freeze pointer is still `55c07cd`,
where the predicate is red.

**Freeze-pointer ambiguity (same family, second instance).** `frozen/FROZEN.md:6` defines the
freeze as "the lane commit that carries this file". That is a set, not a commit: `FROZEN.md`
is byte-identical (`fbabb048…`) at both `55c07cd` and `32a85560`, so a seat that resolves the
pointer the way the file says can legitimately score C2 **PASS** at `32a85560` and **FAIL** at
`55c07cd`. The seat assignment pins `55c07cd`; without that external pin the freeze is
under-determined and the two candidate readings disagree on C2.

## 3. Two further defects in this lane's r49 counters (found while testing (b))

**F2 — C2's load-bearing leg is satisfied by a mutable worktree file.** The counter runs the
sub-checker out of the lane's *working tree*, not the revision:
`tools/check-adjacency-table-r49.py:187` `checker = os.path.join(lane, CHECKER)` and `:188`
`subprocess.run([sys.executable, checker, '--revision', rev], …)`. Every other input is read
through `git show` (`:59`), so this is the one unpinned read. Demonstrated in a fixture clone
at the freeze revision, with **no git write** and the committed blob untouched
(`git show <REV>:tools/check-adjacency-anchors.py | wc -l` → `1211`):

```
$ printf 'import sys\nsys.exit(0)\n' > $D/tools/check-adjacency-anchors.py   # worktree only
$ git -C $D status --porcelain
 M tools/check-adjacency-anchors.py
$ python3 <freeze>/tools/check-adjacency-table-r49.py --revision 55c07cd… --lane $D
{"anchors_checker_rc": 0, "problems": [], "verdict": "PASS"}
```

One uncommitted edit flips the counted verdict FAIL→PASS at a revision whose committed
checker returns 1. The counter cannot distinguish "the anchors are green" from "the worktree
checker said 0". Contrast the C3 counter, which extracts the script it runs from the revision
(`tools/check-fd-band-r49.py:63-64`, `git archive --format=tar rev CENSUS`, used at `:85`) and
pins its child environment (`:96`).

**F3 — inherited `GIT_*` redirects every "frozen bytes" read to another repository.** All
three counters shell out with no `env=`: `check-adjacency-table-r49.py:59`,
`check-scrub-admission-r49.py:131`, `check-fd-band-r49.py:52`. The lane already owns the
allow-list — `tools/_revision.py:62-66` `clean_env()`, applied by `_revision.py:69-73`
(`_git(..., env=clean_env())`) and imported by `tools/check-adjacency-anchors.py:18`
(`from _revision import E_GIT, RevisionError, bind, clean_env`). The r49 counters bypass it. Measured against
the real lane with a fixture repo holding one foreign commit:

```
lane contains it?  fatal: Not a valid object name c79ba052…^{commit}   lane_rc=128
GIT_DIR=<fixture>/.git git -C <lane> cat-file -e c79ba052…^{commit}    env_rc=0
GIT_DIR=<fixture>/.git git -C <lane> show c79ba052…:PROVINCE.md        SENTINEL foreign bytes
```

Content addressed by a genuine sha cannot be forged this way, so the bite is provenance: the
`revision` a counter prints can be a commit the named lane does not contain, while `--lane`
(the documented "names the repo") is silently ignored.

**F4 — C1 and C3 do not share F2/F1; C3 supports, C1 is pending by construction.** C3 at the
freeze: `stale_ok 1, diag_ok 1, band_ok 1, cases 167`, summary
`TSUKUROI_CENSUS_SELFTEST: PASS (167 cases, 167 passed, 0 failed)`, `verdict PASS`, twice
(122 s and 98 s runs). C1 at the freeze: `structural_ok 1, corr_ok 1, quotes_ok 3,
verdicts_ok 0, seats_ok 0, marks_ok 0` → FAIL, exactly the three cohort legs `verdicts_ok /
seats_ok / marks_ok` that cannot exist before w1 lands. C1 reads every content leg through
`show()` (`check-scrub-admission-r49.py:134`) and executes no worktree file, so it is immune
to F2; it shares F3.

## 4. (c) Adjacency-class versus tsukuroi-internal

| finding | class | owner of the fix |
|---|---|---|
| F1, C2 red at freeze (stale IN-109 `found_line`) | **tsukuroi-internal** sequencing (the row is this lane's own `tools/tsukuroi-census.sh` line). **Adjacency-class in consequence**: IN-109 is an *inbound* pointer pinned to `tameshi-shokunin/corpus/knowledge/service-optin-protocol.md:153`, and a post-freeze repin changes what that cross-lane pointer asserts. | tsukuroi re-freezes; the PROVINCE/adjacency owner must know a repin happened after the freeze. |
| F2, worktree sub-checker | **tsukuroi-internal** (counter design) | tsukuroi L1 |
| F3, `GIT_*` inheritance | **tsukuroi-internal** counters; the *pattern* is fleet-wide — kake already hardened (`append_guard.py:53-57`), tsukuroi's `_revision.py:62` already hardened, so no sibling owes this lane anything. | tsukuroi L1 |
| F2', freeze-pointer ambiguity ("the commit that carries this file") | **fleet-class convention**, instantiated here; the same self-referential wording would make any lane's freeze under-determined. | orchestration convention, not a lane |

Nothing found is a sibling lane's breakage; the one adjacency-class item is F1's *consequence*,
not a defect in tameshi's bytes.

## 5. Proposed move (one, bounded)

**Pin C2's borrowed leg to the revision and make the freeze gate read it there: (i) extract
`tools/check-adjacency-anchors.py` from `--revision` into scratch (mirror
`check-fd-band-r49.py:63-64`) instead of executing `os.path.join(lane, CHECKER)`
(`check-adjacency-table-r49.py:187-188`); (ii) route the three counters' git helper
(`:59`, `:131`, and C3's twin) through `tools/_revision.py:62 clean_env()`; (iii) add one
negative case per counter — replace the worktree checker with `sys.exit(0)` and require the
C2 verdict *not* to flip, and run one counter under `GIT_DIR=/nonexistent-selftest-dir` and
require an identical verdict (kake `append_guard.py:531-532` shape); (iv) require the C2
predicate to be green at the *prospective freeze commit itself* before `frozen/FROZEN.md` is
committed.**

Second-order effects, traced:

- The move does **not** manufacture a PASS. C2 still reads FAIL at `55c07cd` — it becomes
  *determinate* instead: a function of `--revision` alone, not of the worktree, the caller's
  environment, or which "commit that carries FROZEN.md" a seat happens to pick.
- Freeze hygiene improves on the axis the lane already polices for C1: `corr_ok`
  (`check-scrub-admission-r49.py`, C7/C8) proves the round-48 corrections are *in the bytes*;
  C2 has no equivalent leg for the registry row it borrows, which is precisely how a stale
  `found_line` reached a freeze commit for the second time (2593→2642 in r48, 2642→2660 in r49).
- Cost is small and mechanical: ~8 lines in C2, a 1-line `env=` in three counters, three
  selftest cases. No new machinery, no new dependency; `clean_env` already exists at
  `tools/_revision.py:62`.
- C1 and C3 verdicts are unchanged by the move (C1 passes no worktree file to a child; C3
  already extracts its script and pins its env).

## 6. Risks

1. **Executing an old checker.** Pinning means a C2 run at an old revision executes the
   checker as of that revision. That is correct for retro-scoring but must be documented next
   to the counter docstring, or a later hardening of `check-adjacency-anchors.py` will look
   "missing" when C2 is re-run at an older rev.
2. **`clean_env()` fixes `PATH=/usr/bin:/bin`** (`tools/_revision.py:65`). C1/C2 shell only
   `git` and `sys.executable` (absolute) today; C3 already uses `/bin/bash` absolutely
   (`check-fd-band-r49.py:97`). Any future relative-binary call would break loudly, which is
   the intended failure mode.
3. **The tempting wrong repair.** Removing `anchors_checker_rc` from the predicate would turn
   C2 green at a revision whose anchor registry is internally inconsistent. Refuse it: the
   leg is what caught F1. The correct repair is the pin plus a freeze gate, not predicate
   surgery.
4. **Freeze-pointer wording.** Replacing FROZEN.md:6's self-reference with an explicit sha
   changes the convention several lanes share; propose it to the orchestrator, do not do it
   inside this round.

## 7. Verification — what I ran, and what I did not

Receipts (all under `.ufo/waves/round-49/w1/R49ConnWave/`):
`c2-at-freeze-55c07cd.json`, `c2-at-32a85560.json`,
`c2-forged-pass-worktree-checker.json`, `frozen-checker-sha.txt`,
`sub-checker-at-freeze.json`, `sub-checker-branchtip-eq-freeze.json`,
`c1-at-freeze-55c07cd.json`, `c3-at-freeze-55c07cd.json`, `git-env-inheritance.txt`.

Commands (absolute lane path, `TMPDIR` in scratch, counters copied out of the freeze with
`git show <REV>:tools/…` so the measuring tool is also the frozen one):

```
python3 $S/tools/check-adjacency-table-r49.py --revision 55c07cd… --lane <lane>   # FAIL, rc 1
python3 $S/tools/check-adjacency-table-r49.py --revision 32a85560… --lane <lane>  # PASS, rc 0
python3 $S/tools/check-scrub-admission-r49.py  --revision 55c07cd… --lane <lane>  # FAIL (cohort legs)
python3 $S/tools/check-fd-band-r49.py          --revision 55c07cd… --lane <lane> --work $S/c3work
                                                                                  # PASS, 167 cases, 2 runs
```

Freeze-blob hashes recorded: `tools/check-adjacency-table-r49.py` = `17be2a11…`,
`tools/check-adjacency-anchors.py` = `a4f500ef…` (identified byte-for-byte with the live
worktree copy, so F2 is a hole, not a present lie).

Not done, and therefore not claimed:
- No C1/C3 selftest-bearing command was run concurrently; C3's two runs were sequential.
- I did not run the control batteries (`controls/battery.py`), did not re-score any control,
  and did not run any counter at the lane tip `d7cfc273`.
- I did not verify the other 15 DRIFTED inbound rows beyond the one blocking row
  (`inbound[108]` / IN-109); only that row is named by a finding.
- No sibling repository was read at anything other than committed bytes, and no sibling tool
  was executed.
- No tool was installed or upgraded (nothing was needed).

## 8. Scratch

Removed before yield: `/fast/scratch/hyaku/tsukuroi-r49/R49ConnWave/` (fixture clones,
counter copies, C3 work dirs). Free space observed at start: `/fast` 487 G free, 40 % used.
