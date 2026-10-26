# GateHeaderRecheck — G-1 command log and observed summaries

Seat: GateHeaderRecheck (L2, round 39 w1). Read-only lane runs; no host mutation.
Scratch: `/fast/scratch/hyaku/tsukuroi-r39/GateHeaderRecheck` (TMPDIR there; removed after receipts copied).
Tools under test (blob hashes identical at base `0eff65b2` and tip `2e1c2a40`):

- `tools/check-knowledge-header.py` blob `e253fd516ee7a77659310470dcc70324c2bc1ff6`
- `tools/check-recheck-commands.py` blob `055f9b3835c7cf89765389918de3ecfaaed9be95`
- `tools/_revision.py` blob `24f398a6b981488218e6cb05c6c1016efa84cf29`
  (`git ls-tree 0eff65b2 …` and `git ls-tree 2e1c2a40 …` printed the same three lines)

## Docstring / --help (read before running)

`python3 tools/check-knowledge-header.py --help` → exit 0

```
usage: check-knowledge-header.py [-h] (--revision REV | --selftest)
                                 [--lane REPO] [--branch BRANCH]
Read-only knowledge-header gate (QUALITY 8).
  --revision REV   required: 7-64 hex commit; HEAD/@/refs are rejected
  --branch BRANCH  branch the revision must be landed on (default: master)
```

`python3 tools/check-recheck-commands.py --help` → exit 0

```
usage: check-recheck-commands.py [-h] (--revision REV | --selftest)
                                 [--paths PATH [PATH ...]] [--exec-log PATH]
                                 [--branch BRANCH] [--forbid LIST]
Read-only recheck-procedure gate (rounds 17-18).
  --paths  knowledge files or directories (default: corpus/knowledge)
```

Exit classes documented in both docstrings: 0 pass / 1 finding / 2 could-not-evaluate.

## Runs — branch tip observed by the binding in every run: `394e1ba4fab39a417abe66a7802f87cf1ff8dd61` (= lane master and origin/master)

Lane cross-check runs (executed in the lane worktree, `--lane .`; the lane's origin ref exists, so `origin_tip` is populated):

| revision | tool | exit | status | summary fields |
|---|---|---|---|---|
| `0eff65b21bb81195ee06c96a83afbd7a07e52eef` (base) | check-knowledge-header | 0 | PASS | `finding_count=0 note_count=59 complete_count=59 clean_count=59` |
| `0eff65b21bb81195ee06c96a83afbd7a07e52eef` (base) | check-recheck-commands | 0 | PASS | `flagged_count=0 file_count=59 clean_count=43 invocation_count=81 pointer_section_count=42 resolved_count=16` |
| `2e1c2a40c13dc52e155d89e72f3fdd560db7399a` (declared tip) | check-knowledge-header | 0 | PASS | `finding_count=0 note_count=60 complete_count=60 clean_count=60` |
| `2e1c2a40c13dc52e155d89e72f3fdd560db7399a` (declared tip) | check-recheck-commands | 0 | PASS | `flagged_count=0 file_count=60 clean_count=44 invocation_count=81 pointer_section_count=42 resolved_count=16` |
| `394e1ba4fab39a417abe66a7802f87cf1ff8dd61` (live lane tip) | check-knowledge-header | 0 | PASS | `finding_count=0 note_count=60 complete_count=60 clean_count=60` |
| `394e1ba4fab39a417abe66a7802f87cf1ff8dd61` (live lane tip) | check-recheck-commands | 0 | PASS | `flagged_count=0 file_count=60 clean_count=44 invocation_count=81 pointer_section_count=42 resolved_count=16` |

Clone runs (`git clone -q --shared <lane> $S/{tip,base}-clone`, `git remote remove origin`, `git -C <clone> checkout -q <rev>`, tool executed from that checkout). Identical numbers, `origin_tip=null` because the clone's origin ref was removed:

| revision | tool | exit | status | summary fields |
|---|---|---|---|---|
| `2e1c2a40` | check-knowledge-header (`--lane <clone>`) | 0 | PASS | `finding_count=0 note_count=60 complete_count=60 clean_count=60` |
| `2e1c2a40` | check-recheck-commands | 0 | PASS | `flagged_count=0 file_count=60 clean_count=44 invocation_count=81` |
| `0eff65b2` | check-knowledge-header (`--lane <clone>`) | 0 | PASS | `finding_count=0 note_count=59 complete_count=59 clean_count=59` |
| `0eff65b2` | check-recheck-commands | 0 | PASS | `flagged_count=0 file_count=59 clean_count=43 invocation_count=81` |

Targeted run (the only knowledge addition in the delta, alone):

`python3 tools/check-recheck-commands.py --revision 2e1c2a40… --paths corpus/knowledge/pacman-transaction-order-r39.md` → exit 0
`{"status":"PASS","file_count":1,"flagged_count":0,"clean_count":1,"invocation_count":0,"pointer_section_count":0,"resolved_count":0}`

Selftests (`--selftest`, both tools, exit codes captured without a pipe):

- `check-knowledge-header.py --selftest` → exit 0, `{"selftest":{"cases":25,"failures":[],"passed":25,"status":"PASS"}}`
- `check-recheck-commands.py --selftest` → exit 0, `{"selftest":{"cases":95,"failures":[],"passed":95,"status":"PASS"}}`

## Delta analysis (base → declared tip)

`git diff --name-status 0eff65b2 2e1c2a40 -- corpus/knowledge/ corpus/SOURCES.md corpus/QUALITY.md`:

```
M  corpus/SOURCES.md
M  corpus/knowledge/adjacency-anchors-r19.json
A  corpus/knowledge/pacman-transaction-order-r39.md
```

`git diff 0eff65b2 2e1c2a40 --stat -- tools/` shows no change to either gate (only `tools/check-transaction-order-r39.py`, `tools/score-storage-hidden-r39.py` added and `tools/tsukuroi-census.sh` modified).

The knowledge-header gate's note-set diff base→tip is exactly one added note:

```
{"lines": {"recheck": 3, "source": 1, "verified-at": 2}, "path": "corpus/knowledge/pacman-transaction-order-r39.md", "problems": []}
```

Head lines of that file (`corpus/knowledge/pacman-transaction-order-r39.md:1-3`, 58 lines, sha256 `701a462dfe9c3d03fba0366719e772e081d6cb181e25398d78c0f1ebf5b0d74a`): `source:` (S208/S213–S218), `verified-at: 2026-10-26`, `recheck:` with `on-release` and `30d`. The recheck command is `python3 tools/check-transaction-order-r39.py --revision <REV>` — `python3` is not in the default forbid list (`pacman,checkupdates,yay,paru,mkinitcpio,limine-update`).

Live tip `394e1ba` differs from the declared tip only by `.ufo/waves/round-39/make-w1-spec.py`, `.ufo/waves/round-39/revs.json` and `w1` spec entries: `git diff --name-only 2e1c2a40 394e1ba -- corpus tools` → 0 lines. Gate inputs are therefore identical at both.

## Receipts

`kh-*.json`, `rc-*.json` (full stdout JSON), `*.err` (all empty), plus this summary.
