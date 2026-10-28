VERDICT: defect-found

Scope sentinel for wave w1 (item N-2). No blocking defect: lane diff is in write scope, no fleet/MANIFEST/state contact, no network/sudo/shell=True/credential reads, no /tmp literal. Three minor calibration/scope defects below. Raw receipts: .ufo/waves/round-51/w1/R51SentScope/sentinel-receipts.txt. No installs or updates were made.

## (a) Lane diff c0ad548a..2732ee6c — IN SCOPE
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff c0ad548a93425a3bf8813d28d92f26fe2f64b9d4 2732ee6c06108c031c4d8043239b994e0504eb2f --name-status` lists 21 paths:
- `.ufo/waves/round-51/before/*` (10 A), `.ufo/waves/round-51/controls/battery.py`, `.ufo/waves/round-51/frozen/{FROZEN.md,FROZEN-hashes.txt}` — in scope (`.ufo/waves/round-51`).
- `M SCORECARD.md`, `M SKILL.md`, `M corpus/knowledge/btrfs-scrub-grounding-r45.md` — in scope.
- `A tools/{check-adjacency-table,check-scrub-admission,check-selftest-matcher,lint-grounding,score-counter-cheats}-r51.py` — in scope (`tools/`).
- None touches MANIFEST.json, fleet templates/scripts, or `.ufo/state`.

## (b) Fleet root — NOT TOUCHED; paths for L1
`git -C /home/vgpnk/Projects/shokunin status --porcelain` shows 41 entries; `diff --stat` 41 files, 24475+/4-. Fleet paths whose content mentions tsukuroi / round-51 / R51:
- `/home/vgpnk/Projects/shokunin/.scratch/goal-20261028-hyaku-run11.md` — MODIFIED (uncommitted), names tsukuroi at lines 36, 77, 82. Not round-51-specific; owned by the operator/fleet.
- `/home/vgpnk/Projects/shokunin/.scratch/closure-r54/lane/.ufo/evidence/**` — untracked; many files contain tsukuroi/round-51 strings (e.g. `.../kaika-round-1/sources-census-final.txt`, `.../round-16/measure-09ee1d0.json`).
- `/home/vgpnk/Projects/shokunin/lane3/` — untracked, 125 matching files (e.g. `lane3/.ufo/waves/round-25/build-spec.json`).
- `/home/vgpnk/Projects/shokunin/tools/` — untracked; contains only `tools/round-49/`, no r51 content.
- Committed fleet round-51 namespace (separate tree from lane `.ufo/waves/round-51`): `.ufo/reports/round-51/{chousa,kake,kama,kengaku,kotoba,kotodama,kumitate,mado,mori,tameshi}.md`, `.ufo/prompts/*round-51.md`. Path-name collision risk only; no file collision.
- `.ufo/waves/round-56/` (untracked) — no matches. Whole-fleet pattern count (excluding the lane dir and .git): 18923 files, mostly committed reports.

## (c) New tools and battery — scope scan
- Network / sudo / shell=True / credentials: none. Greps over the five r51 tools and battery.py return only `subprocess.run` calls on `git`, `bash`, or the counter children.
- Hardcoded `/tmp`: none (`grep -n '/tmp' tools/*r51*.py .../controls/battery.py` empty).
- Writes:
  - `tools/check-selftest-matcher-r51.py:125-126` mkdtemp under `--scratch`; census env `TMPDIR`/`HOME` sandboxed under work at `:149-152`; rmtree `:196`. Compliant.
  - `tools/score-counter-cheats-r51.py:99-100` mkdtemp under `--scratch`; rmtree `:147`. Compliant.
  - `.ufo/waves/round-51/controls/battery.py:245` default `--scratch /fast/scratch/hyaku/tsukuroi-r51/controls`; mkdtemp `:250`; rmtree `:267`. Compliant.
  - `tools/lint-grounding-r51.py`, `tools/check-scrub-admission-r51.py`: read-only (`git show`, override reads).
  - `tools/check-adjacency-table-r51.py:248-253` — see defect D3.
- Census (`tools/tsukuroi-census.sh` at 2732ee6): selftest writes only under `${TMPDIR:-/tmp}` mktemp (census lines 411-416, 604-606); live mode creates no files (line 348). Matcher counter sandboxes this via TMPDIR/HOME (above). Compliant.

## (d) Do the C2/C3 counters write into lane or sibling repos?
- `check-adjacency-table-r51.py`: no writes into lane or sibling repos. Sibling reads are `git -C <sibling> show <commit>:PROVINCE.md` (`:78-80`, read-only), with siblings_root defaulting to `/home/vgpnk/Projects/shokunin` (`check-adjacency-table-r50.py:80` via `R50.SIBLINGS`; `r51:307`). Writes only the two temp files in D3.
- `score-counter-cheats-r51.py`: no writes into lane or sibling repos. Writes only under `--scratch` (`:99-100`, `:147`). Reads lane via `git show` (`:93`).

## Defects (calibration / scope; none blocking)
- D1 — counted C2/C3 bind the WORKING-TREE counter code, not the revision bytes. `score-counter-cheats-r51.py:91` `counter = os.path.join(lane, a.counter)` and `:92` `r50 = os.path.join(lane, 'tools/check-selftest-matcher-r50.py')`; `check-adjacency-table-r51.py:68-69, :222, :265` load r50 from `HERE`. Only the census and table/registry inputs are revision-pinned. Right now `git diff --quiet 2732ee6c... -- tools` is clean (rc 0), so no present defect. Condition: a counted run must execute from a tree at REV (e.g. `git clone --shared` checked out at REV under scratch), or the verdict does not bind the counter code. L1 decides.
- D2 — the lane working tree was written into. `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/__pycache__/` exists (ignored by `.gitignore:2`), with mtime 18:02, the same time as the freeze battery summaries. Importing the r50/r51 modules from `tools/` creates it. Not tracked and not committed, but a read-only seat must not leave it. Proposed fix: `PYTHONDONTWRITEBYTECODE=1` for every counted or seat run, and a clean-up of `tools/__pycache__` by the L1. I ran no counter; I did not create it.
- D3 — `check-adjacency-table-r51.py:248-253` uses `tempfile.NamedTemporaryFile(delete=False)` with no `dir=`. The files go to `$TMPDIR` or `/tmp`, not `--scratch`. They are unlinked at `:275-276`, but the creations sit before the `try`, so an exception in between leaks them. Proposed fix: create them in a `tempfile.mkdtemp()` inside the `try` and `shutil.rmtree` it in `finally`, or pass the scratch dir.

No measurement was run by this seat (sentinel only). The census `--selftest` and the counters were not executed by me.
