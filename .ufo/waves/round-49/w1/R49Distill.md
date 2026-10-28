VERDICT: defect-found

# R49Distill — P-4 artifact provenance check (round 49, w1)

Seat class EXEC-AUTHORIZED (commands named in the item only: `git cat-file -e`, plus read-only
`git show`/`ls-tree`/`log`/`rev-list`/`status`/`diff` and file reads used to locate the named
artifacts). No counter, selftest, battery or reporter was run: every number below is read from
committed bytes or from the working tree, never re-measured. No `lsp` device is mounted in this
seat (tool inventory: read, bash, edit, eval, glob, grep, task, wait, web_search, write), so no
semantic-checker is available; this item is a git-provenance check over `.md`/`.jsonl`/`.py`
artifacts, where no language server would answer anyway. Scratch
`/fast/scratch/hyaku/tsukuroi-r49/R49Distill/` removed at exit; free space seen 506 G on `/fast`.

Freeze revision `55c07cd3f8bff2e12117c34d57b4c618de74d85c` (`git cat-file -t` → `commit`,
`git merge-base --is-ancestor 55c07cd3 HEAD` → true, contained in `refs/heads/master` and
`refs/remotes/origin/master`). Lane tip at the check: `master = HEAD = d7cfc27308e8af51b76b5cfe0c656acc1788cefb`
(HEAD detached from `a330fb0d`, same commit as `master`). Round start base `6256760d…` exists
(`git cat-file -e 6256760d…^{commit}` → ok).

## 1. Existence matrix (`git -C <lane> cat-file -e <REV>:<path>`)

| Artifact | freeze `55c07cd3` | HEAD `d7cfc273` | citable? |
|---|---|---|---|
| freeze commit `55c07cd3…` | — | — | **yes** (commit object, in `master`) |
| `tools/check-scrub-admission-r49.py` | yes | yes (same blob `240bef1e28f2`) | **yes, at freeze** |
| `tools/check-adjacency-table-r49.py` | yes | yes (same blob `48febb0be2a0`) | **yes, at freeze** |
| `tools/check-fd-band-r49.py` | yes | yes (same blob `dd28e9596f87`) | **yes, at freeze** |
| `.ufo/waves/round-49/frozen/FROZEN.md` | yes | yes (amended, see §3 F4) | **yes, at freeze** |
| `.ufo/waves/round-49/controls/battery-summary-r49-c1.jsonl` | **NO** | yes | only at `d7cfc273`+ |
| `.ufo/waves/round-49/controls/battery-summary-r49-c2.jsonl` | **NO** | yes | only at `d7cfc273`+ |
| `.ufo/waves/round-49/controls/battery-summary-r49-c3.jsonl` | **NO** | yes | only at `d7cfc273`+ |
| `.ufo/waves/round-49/controls/battery.py` | **NO** | yes | only at `32a85560`+ |
| `.ufo/waves/round-49/` (wave dir) | tree, 2 files | tree, 11 files | see §3 F3 |
| `.ufo/waves/round-49/w1/` | **NO** (absent) | tree, 1 file (`w1/swarm-registry.json`) | partial only |
| `.ufo/waves/round-49/w1/R49RevGR*.md`, `R49CritGR*.md` (18) | **NO** | **NO** | **no** |
| `.ufo/waves/round-49/w1/R49CritFdB/matrix.txt` (receipt sample) | NO | NO | **no** |
| `.ufo/waves/round-49/w1-results.json` | **NO** | **NO** | **no — file does not exist at all** |
| `.ufo/waves/round-49/before/c1-at-base.json` / `-c2-` / `-c3-` | NO | NO | **no** |
| `.ufo/waves/round-49/before/sources-census-start.txt` | yes | yes | **yes, at freeze** |
| `.ufo/waves/round-49/w1-dispatch.json`, `w1-spec.json`, `make-w1-spec.py` | NO | yes | only at `32a85560`+ |
| `.ufo/waves/round-49/l1-summary.py`, `w1.ready`, `w1.ready.partial` | NO | NO | **no** |

Freeze contents of the wave dir (`git ls-tree -r --name-only 55c07cd3 -- .ufo/waves/round-49`, 2 lines):
`.ufo/waves/round-49/before/sources-census-start.txt` and
`.ufo/waves/round-49/frozen/FROZEN.md`. HEAD adds `controls/{battery.py,battery-summary-r49-c{1,2,3}.jsonl}`,
`make-w1-spec.py`, `w1-dispatch.json`, `w1-spec.json`, `w1-validate.log`, `w1/swarm-registry.json` (11 paths).

## 2. Working-tree-only artifacts (snapshot `2026-10-28T14:44:52-03:00`, lane repo)

`git status --porcelain --untracked-files=all -- .ufo/waves/round-49`, categorised:

| Category | count |
|---|---|
| seat report `.md` under `w1/` | 59 |
| seat receipt files under `w1/<seat>/` | 591 |
| `before/c{1,2,3}-at-base.json` | 3 |
| other (`l1-summary.py`, `w1.ready`, `w1.ready.partial`) | 3 |

The 18 counted C1 seats all exist as files (18/18) in the working tree only. The wave is live: spec
declares `counts {spawn 73, resume 0, total 73}` (`.ufo/waves/round-49/w1-dispatch.json`), 59 reports were
on disk at the snapshot, 14 dispatched seats had not written one yet
(`R49RevCounter, R49ExecFdB, R49CritAssim, R49SentScopeB, R49SentSeat, R49Distill, R49Simplify,
R49ExecGates, R49ExecLiveCensus, R49ScoutHost, R49RevMarks, R49ScoutSources, R49ExecSelfAssess,
R49ScribeCoverage`).

One tracked modification exists in the whole repo: `corpus/SOURCES.md` (working tree only) appends
`, corpus/lessons/round-49.md` to the S255 lesson column. The S255 row itself is committed at the freeze;
the round-49 lesson link is not citable until it is committed with the lesson.

## 3. Findings, by severity

### F1 (blocker) `w1-results.json` does not exist — C1 is unmeasurable on committed bytes
The frozen C1 counter reads exactly `<WAVES>/w1-results.json`
(`55c07cd3:tools/check-scrub-admission-r49.py:350`: `res = load_json(lane, rev, f'{WAVES}/{WAVE}-results.json', a.results_file)`;
`WAVES` at `:55`, `WAVE = 'w1'` at `:56`) and `seats_ok` counts completed entries (`:383`). Round 49 has no
such file: `find . -name 'w1-results.json'` returns rounds 37-48 only, and
`git rev-list --all --objects | grep -c 'round-49/w1-results'` → `0`. FROZEN.md's cohort rule also binds each
seat to "one completed entry of `w1-results.json`" (`55c07cd3:.ufo/waves/round-49/frozen/FROZEN.md:38`).
Consequence: `seats_ok == 18` cannot be reached at any revision until that file is written **and committed**;
the round must not report the C1 predicate as satisfied before then.

### F2 (blocker, QUALITY-class) before-state receipts exist in no revision at all
`before/c{1,2,3}-at-base.json` are untracked and appear in **no** git object:
`git rev-list --all --objects | grep -c "c1-at-base.json"` → `0`. They are cited as the before vector by
`w1/R49ScribeScore.md:26` ("`before/c1-at-base.json`, `c2-at-base.json`, `c3-at-base.json` | direct reads"),
`:74`, `:86`, `:87`, `:88`, and `w1/R49ConnClaims.md:89`. A draft that cites them cites bytes no reader can
reach from the repo — the exact defects this item exists to catch. Either commit them (they are inside the
wave dir, so no lane-policy objection) or replace the citation with a re-runnable command at `6256760d`.

### F3 (quality) The whole `w1/` dir is uncommitted; the round's evidence lives in the working tree
Only `w1/swarm-registry.json` is committed (at `d7cfc273`, absent at freeze). All 59 seat reports and 591
receipts are untracked. Every counted binding — including the 18 `ROW GRn VERDICT`/`SECTION SHA256` lines the
C1 counter reads via `git show <rev>:<WAVES>/w1/<seat>.md` (`:290`) — is currently unreadable from any
commit, so C1's `verdicts_ok`/`seats_ok` measured now would be 0 by construction. Receipts such as
`R49ConnClaims/anchors-checker-at-{base,freeze,master}.json` (cited at `R49ConnClaims.md:89`) are likewise
working-tree only. This is expected mid-wave (14 seats still running) but must be resolved by the integration
commit before the round report names the wave dir.

### F4 (provenance precision) Controls and the amended FROZEN.md exist only from `d7cfc273`, not from the freeze
`git ls-tree 55c07cd3 -- .ufo/waves/round-49/controls` is empty, yet the frozen bytes already promise them:
`55c07cd3:.ufo/waves/round-49/frozen/FROZEN.md:41` — "## Pre-data controls (frozen counters; receipts in
`.ufo/waves/round-49/controls/`)". They land in `d7cfc273` ("round-49: pre-data control batteries … at
32a85560"), which also appends a "## Control outcomes (scored at `32a85560`…)" section to FROZEN.md
(`git diff 55c07cd3 HEAD -- …/frozen/FROZEN.md` → 8 insertions; `git log 55c07cd3..HEAD --
…/frozen/FROZEN.md` → `d7cfc273` only). Consequence: any report that pins
`controls/battery-summary-r49-c{1,2,3}.jsonl` to `55c07cd3` fails — `cat-file -e` exits 128 (independent
confirmation: `w1/R49ScoutQuality.md:24,31`). They are citable **at `d7cfc273` or later**; the receipt contents
agree with the FROZEN prose (c1 8 lines K0-K6 FAIL + K-pass PASS; c2 5 lines K0-K3 FAIL + K-pass PASS; c3
4 lines K0-K2 FAIL + K-pass PASS), so the evidence exists — only the pin must be right.

### F5 (record defect) The stated row-hash convention is wrong for all three rows
`FROZEN.md:19` says "LF-joined row lines, no trailing LF"; the counter docstring repeats it
(`55c07cd3:tools/check-scrub-admission-r49.py:33-34`), while `section_hashes` hashes
`'\n'.join(lines[i:j])` (`:187`) where `j` is the next `## ` heading, so the text ends with the blank
separator's newline. Recomputed from the freeze bytes (independent):

| Row | published | with trailing LF | no trailing LF |
|---|---|---|---|
| GR1 | `3a2ba180…fee1` | `3a2ba180…fee1` ✓ | `0b67bea0…` ✗ |
| GR2 | `d4296085…027f` | `d4296085…027f` ✓ | `75d24ea6…` ✗ |
| GR3 | `43430a14…c32c` | `43430a14…c32c` ✓ | `17b19a53…` ✗ |

The published values are reproducible, so no row byte is wrong — but a seat that follows the documented
convention gets a mismatch on every row and could mis-report a defect (or bind a hash the counter rejects).
Same observation, independently, at `w1/R49CritGR2b.md:8`. Fix the two prose sites, or the hash definition,
in one place.

### F6 (claim C1 blocked by its own rule) `R49CritGR2b` binds a negative on the current hash
`w1/R49CritGR2b.md:1` is `ROW GR2 VERDICT: partly`, line 2 is `SECTION SHA256: d4296085…027f` — the frozen
GR2 hash. It is the only non-`holds` line among the 18 (`grep -n "^ROW GR[123] VERDICT:" w1/R49{Rev,Crit}GR*.md`
returns exactly that one after excluding `holds$`); the other 17 read `holds` against the matching frozen
hashes. FROZEN.md's own rule: "A bound-format negative (`partly`/`fails`) on the current hash blocks the row
whatever its citations" (`FROZEN.md:36`). Therefore `verdicts_ok` is at most 2 and C1's predicate
(`verdicts_ok == 3`) cannot hold as the cohort stands. Reported here because it is the provenance of the
round's headline claim, not a row-bytes opinion; the row itself is out of this seat's scope.

## 4. Checks that came out clean (with the command that shows it)

1. **No drift on the frozen instruments.** `git rev-parse 55c07cd3:<f>` == `git rev-parse HEAD:<f>` for all
   three counters (`240bef1e28f2`, `48febb0be2a0`, `dd28e9596f87`) and for `FROZEN.md`'s base text; working-tree
   copies hash identically (`sha256sum`). `git diff --stat 55c07cd3 HEAD -- corpus/knowledge/btrfs-scrub-grounding-r45.md
   PROVINCE.md tools/tsukuroi-census.sh corpus/SOURCES.md` → empty, so the claim surfaces are unchanged since the freeze.
2. **Counters produce no receipt files, hence nothing outside `.ufo/waves/round-49/`.**
   `grep -nE "open\([^)]*'w|…'wb'|write_text|write_bytes"` over the three frozen counters → `NONE`; they print
   JSON to stdout. `check-fd-band-r49.py` builds its work dir under `--work` /
   `$HYAKU_SCRATCH/tsukuroi-r49/counter-c3` (default `/fast/scratch/hyaku`, `:56-57`), points the census
   selftest's `TMPDIR` at `work/run` (`:96`) and removes the tree in `finally` (`:118`) — never `/tmp`.
   `check-adjacency-table-r49.py` opens only `'rb'` (`:65`). The only round-49 writer is the controls harness
   `controls/battery.py`, which writes `<lane>/.ufo/waves/round-49/controls/battery-summary-r49-<claim>.jsonl`
   (`:8`, `:282`) from scratch under `$HYAKU_SCRATCH/tsukuroi-r49/controls` (`:31`, rmtree `:286`).
3. **No `/tmp` path is offered as evidence anywhere in the wave.** The only `/tmp` strings in `w1/*.md` are
   `R49ScribeSkill.md:181-183`, quoting `SKILL.md:481-482` prose. The 49 `/fast/scratch/…` mentions are scratch
   paths in commands plus "removed on exit" statements; one receipt path was checked and resolves inside the
   wave dir (`R49ExecFdA.md:37` → `w1/R49ExecFdA/matrix.txt`).
4. **`SCORECARD.md` is committed and unchanged** (`git rev-parse 55c07cd3:SCORECARD.md` == `…HEAD:…`); its
   `:3138` reference to `battery-summary-r49-c{1,2,3}.jsonl` is resolvable at `d7cfc273`, so that line is
   citable — it just must not be pinned to the freeze.

## 5. Uncitable artifacts, as requested

Working tree only, no revision anywhere (each was checked with `git cat-file -e` at `55c07cd3` and `HEAD`,
and for the `before/` files additionally against `git rev-list --all --objects`):

```
.ufo/waves/round-49/before/c1-at-base.json          (cited: R49ScribeScore.md:26,40,74,86-88; R49ConnClaims.md:89)
.ufo/waves/round-49/before/c2-at-base.json          (same)
.ufo/waves/round-49/before/c3-at-base.json          (same)
.ufo/waves/round-49/w1-results.json                 (absent entirely; C1 counter:350 needs it)
.ufo/waves/round-49/l1-summary.py                   (cited: R49ScribeLesson.md, R49ScribeScore.md, R49SentForge.md)
.ufo/waves/round-49/w1.ready, w1.ready.partial
.ufo/waves/round-49/w1/<59 seat reports>.md         (incl. all 18 counted C1 bindings)
.ufo/waves/round-49/w1/<seat>/<591 receipt files>   (incl. R49ConnClaims/anchors-checker-at-{base,freeze,master}.json)
corpus/SOURCES.md modification (S255 → corpus/lessons/round-49.md link only)
```

Citable only at a later pin, not at the freeze: the three `controls/battery-summary-r49-*.jsonl`,
`controls/battery.py`, the FROZEN.md "Control outcomes" section (`d7cfc273`)(`32a85560` for `battery.py`),
`w1-dispatch.json`, `w1-spec.json`, `make-w1-spec.py`, `w1/swarm-registry.json`.

Verdict for the item's question: **the round's report may cite, at the freeze, exactly the freeze commit, the
three counters, `FROZEN.md` (pre-`d7cfc273` text), and `before/sources-census-start.txt`** — everything else
in the round's evidence chain needs either the `d7cfc273` pin (controls) or must be committed first (the whole
`w1/` dir, `w1-results.json`, the `before/` vectors).

## 6. Residual risk / not done

- I did not run any counter or selftest (out of this seat's command grant), so the predicates are **not**
  re-measured here; §3 F1/F6 are read from committed counter code, the FROZEN text and the seat files.
- The wave is live (14 of 73 seats unwritten). Counts in §2 are a timestamped snapshot; F1/F3 may be resolved
  by the integration commit — the finding is the state at `2026-10-28T14:44:52-03:00`, and the report must not
  be written against anything older.
- F5's mismatch is a documentation defect only; I verified the published hashes reproduce from freeze bytes,
  so no row content is implicated by this seat.
