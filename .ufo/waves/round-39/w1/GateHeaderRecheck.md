VERDICT: supports

# GateHeaderRecheck — item G-1 (lane gates A)

## What was run

Both gates were run read-only, at the declared frozen tip `2e1c2a40c13dc52e155d89e72f3fdd560db7399a` and at base `0eff65b21bb81195ee06c96a83afbd7a07e52eef`, plus (extra) at the live lane tip `394e1ba4fab39a417abe66a7802f87cf1ff8dd61`. Docstrings and `--help` were read first (exit 0 for both helps); exit classes 0 pass / 1 finding / 2 could-not-evaluate come from the docstrings (`tools/check-knowledge-header.py:35`, `tools/check-recheck-commands.py:38`).

Every run executed inside the lane worktree with the lane's own refs (`--branch` default `master`, observed `branch_tip = 394e1ba4fab39a417abe66a7802f87cf1ff8dd61` = `git rev-parse master origin/master`), and was repeated from `git clone --shared` checkouts of each revision with `origin` removed; both routes produced identical numbers. Receipts: `.ufo/waves/round-39/w1/GateHeaderRecheck/` (`summary.md` holds the verbatim command log, full stdout JSON in `kh-*.json` / `rc-*.json`, all `*.err` empty).

## Summaries and exit codes (in-lane runs; clone runs identical except `origin_tip: null`)

Base `0eff65b2`:

- `python3 tools/check-knowledge-header.py --revision 0eff65b2… --lane .` → **exit 0**, `status PASS`, `finding_count=0`, `note_count=59`, `complete_count=59`, `clean_count=59`.
- `python3 tools/check-recheck-commands.py --revision 0eff65b2…` → **exit 0**, `status PASS`, `flagged_count=0`, `file_count=59`, `clean_count=43`, `invocation_count=81`, `pointer_section_count=42`, `resolved_count=16`.

Declared tip `2e1c2a40`:

- `… check-knowledge-header.py --revision 2e1c2a40… --lane .` → **exit 0**, `status PASS`, `finding_count=0`, `note_count=60`, `complete_count=60`, `clean_count=60`.
- `… check-recheck-commands.py --revision 2e1c2a40…` → **exit 0**, `status PASS`, `flagged_count=0`, `file_count=60`, `clean_count=44`, `invocation_count=81`, `pointer_section_count=42`, `resolved_count=16`.

Live lane tip `394e1ba` (same inputs as the declared tip, see below): both tools **exit 0 / PASS**, `note_count=60 clean_count=60` and `flagged_count=0 file_count=60 clean_count=44 invocation_count=81`.

Targeted run of the single round-39 knowledge addition: `check-recheck-commands.py --revision 2e1c2a40… --paths corpus/knowledge/pacman-transaction-order-r39.md` → **exit 0**, `{"status":"PASS","file_count":1,"flagged_count":0,"clean_count":1,"invocation_count":0}`.

Selftests (the gates themselves are sound at this blob): `--selftest` → **exit 0** for both, `25/25` cases (`kh-selftest.json`) and `95/95` cases (`rc-selftest.json`), zero failures.

## Red at tip, green at base?

**None.** No finding of either class appeared at any revision: `findings: []` in all six gate runs, `flagged_count=0` throughout. There is consequently no round-39 file to name as a cause. Both gates are strictly no-worse at the tip: the knowledge-header note set grew by exactly one note and that note is clean.

## Why the delta cannot be tool drift

`git ls-tree 0eff65b2 …` and `git ls-tree 2e1c2a40 …` print the same blobs for `tools/check-knowledge-header.py` (`e253fd516ee7a77659310470dcc70324c2bc1ff6`), `tools/check-recheck-commands.py` (`055f9b3835c7cf89765389918de3ecfaaed9be95`) and `tools/_revision.py` (`24f398a6b981488218e6cb05c6c1016efa84cf29`); `git diff 0eff65b2 2e1c2a40 --stat -- tools/` shows no touch to either gate. The comparison is content-only.

## The one content change in gate scope

`git diff --name-status 0eff65b2 2e1c2a40 -- corpus/knowledge/ corpus/SOURCES.md corpus/QUALITY.md`:

```
M  corpus/SOURCES.md
M  corpus/knowledge/adjacency-anchors-r19.json
A  corpus/knowledge/pacman-transaction-order-r39.md
```

`corpus/SOURCES.md` and the `.json` are outside both scopes (the header gate reads `*.md` under `corpus/knowledge/`: `tools/check-knowledge-header.py:8-9`; the recheck gate expands directories to `*.md`: `--paths` help). The note-set diff base→tip is exactly:

```
{"lines": {"recheck": 3, "source": 1, "verified-at": 2}, "path": "corpus/knowledge/pacman-transaction-order-r39.md", "problems": []}
```

Its three header keys sit at `corpus/knowledge/pacman-transaction-order-r39.md:1-3` (`source:` S208/S213–S218, `verified-at: 2026-10-26`, `recheck:` with `on-release` for S208/S213–S217 and `30d` for S218), so the QUALITY 8 header requirement is met by the new entry; file is 58 lines, sha256 `701a462dfe9c3d03fba0366719e772e081d6cb181e25398d78c0f1ebf5b0d74a`.

## Observations (not findings)

1. The new entry's recheck command is `python3 tools/check-transaction-order-r39.py --revision <REV>`; `python3` is not in the default forbid list, and the gate reports `invocation_count=0` for that file. This is ordinary gate behaviour, not a round-39 regression: `check-recheck-commands.py --revision 0eff65b2 --paths corpus/knowledge/adjacency-anchors-r19.md` also reports `invocation_count=0` at base, and the global count is unchanged (`81` at base and at tip) despite the added file.
2. The live lane tip is two commits past the declared tip, but `git diff --name-only 2e1c2a40 394e1ba -- corpus tools` → 0 lines (the delta is `.ufo/waves/round-39/make-w1-spec.py`, `revs.json`, `w1` spec files), so the tip verdict holds for the live tip as well — measured directly, not inferred.
3. The uncommitted worktree modification `M PROVINCE.md` and the untracked `.ufo/waves/round-39/w1/` directory do not affect either gate: both bind to a committed revision.
4. Concurrent sibling activity is visible in the lane worktree and is not mine: `git status --porcelain` at seat start showed ` M PROVINCE.md`, `?? .ufo/waves/round-39/w1-dispatch.err`, `?? .ufo/waves/round-39/w1/`; by 03:05 it also showed ` M SKILL.md` (`git diff --stat SKILL.md` → `1 file changed, 21 insertions(+)`, mtime 03:03:26) and `?? .ufo/waves/round-39/w1.ready.dispatched`, and `tools/__pycache__/check-transaction-order-r39.cpython-314.pyc` appeared at 03:04:16. I never ran that tool; both gates I ran set `sys.dont_write_bytecode = True` (`tools/check-knowledge-header.py:44`, `tools/check-recheck-commands.py:54`) and left no `.pyc` of their own (`tools/__pycache__` holds `_revision`/`check-*` caches from 01:11–02:09 and 03:04:16, no `check-knowledge-header` or `check-recheck-commands` entry). Flagged, not remediated: lane content is read-only for this seat.

## Risks / limits

- Both gates are structural (header keys present and valued; no forbidden binary in the operative `recheck:` line). Green here says nothing about whether the TO1–TO8 rows are true — that is the C2 reviewer kill rule (QUALITY 81), not this seat's item; I judged no TO row.
- I did not run `--exec-log`; the item did not ask for it, and no lane log was named.

## Host and lane hygiene

No lane file was created, edited or deleted; no git or jj mutation in the lane; no host action, no sudo, no pacman (transactions remain paused). Scratch `/fast/scratch/hyaku/tsukuroi-r39/GateHeaderRecheck` (TMPDIR there) was removed after receipts were copied. No tool was installed or upgraded.
