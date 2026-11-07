# Draft — round-90 lesson `## Mistakes` (seat ScribeLesson)

Measured at lane revision `ce89df93e5f576c5c236d4547299e9ea954e8853` (`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`), pre-round tip `c0f91856a5cc4816ae5d075022f16dc6aef0593c`, freeze `6511437e7d86d3f1e7e39a45df91ade1d8293612`. Every execution was made from a `git clone --shared` at `/fast/scratch/hyaku/tsukuroi-r90/ScribeLesson/lane` (HEAD `ce89df93`); the lane was not written, no `sudo`, no host write. Raw receipts: `.ufo/waves/round-90/w1/ScribeLesson/receipts/` (`commands.txt`, `new-runs0.out/.err`, `old-battery-runs0.out/.err`, `old-counter-runs0.out`, `old-counter-runs0.json`). Row shape: `class · evidence pointer · captured-by · fix · shown-able-to-fail`.

| Class | Evidence pointer | Captured-by | Fix | Shown able to fail |
|---|---|---|---|---|
| **M1 — `R89-EMPTY-RUNS-MET`**: an instrument's CLI accepts a degenerate argument that empties the evidence set, so the verdict is vacuous. The r89 counter declared `--runs` with no floor, built zero runs from it, and returned `verdict met` / rc 0 through `all()` over an empty sequence; the r89 battery had the same shape and exited 0 with no output. | `7f3f30b3:tools/battery-discrimination-r89.py:275` (`ap.add_argument("--runs", type=int, default=3)` — no floor), `:303` (`runs = [run_once(...) for _ in range(a.runs)]` — zero iterations), `:307-308` (`met = errors == 0 and all(... for r in runs)` — empty ⇒ `True`), `:322` (`return {"met": 0, ...}[verdict]`); same shape at `7f3f30b3:tools/limine-pin-battery-r89.py:1112`, `:1128`, `:1135` (rc 0, no output). Filed by `.ufo/waves/round-89/w1/CriticClaims.md:104-113` ("`all()` over an empty list is `True`"); routed by `corpus/lessons/round-89-verifier-spotcheck.md:127-128` ("count `--runs 0` as void"); the r89 lesson carried it only as routed `R89-R1` (`corpus/lessons/round-89.md:81`), never as a Mistakes row. Resolution: `git log --oneline -3 -- tools/battery-discrimination-r89.py` → `fba764ca` (freeze commit; bytes identical at `7f3f30b3`, `git diff --stat fba764ca 7f3f30b3 -- …` empty); `-- tools/limine-pin-battery-r89.py` → `81f68d00` (candidate). | `none`: QUALITY 1-129 add no domain check for an instrument's own counting arguments. Nearest: 114 freezes controls but does not require a degenerate-argument control; 116 refuses a malformed digest on every input path, not a count that empties the evidence; 126 judges whether a control's verdict was computed, and zero runs give no control row. | Round 90's counting instrument `tools/limine-pin-battery-r90.py` (sha256 `8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5`, frozen at `6511437e`, `.ufo/waves/round-90/before/freeze-manifest.sha256:1`) refuses `--runs < 1` at `:1572` (`if not a.gate or a.runs < 1: ap.print_usage(sys.stderr); return 2`) and declares `--runs N>=1` at `:112`; `--runs 0` exits 2 before any fixture is generated, stdout empty. The r89 counter is retired unmodified (no counter is used this round; `R89-R1` stays routed). Residual: no committed control invokes the guard (`before/controls/run-controls.sh:22` runs only `--runs 3`) — add `K3-runs0-usage` (rc 2, no verdict line) to the next freeze. | **Old state, r89 battery:** `python3 <7f3f30b3:tools/limine-pin-battery-r89.py> --gate tools/check-limine-pins.py --runs 0 --work …` → `rc=0`, stdout empty, stderr empty (vacuous pass). **Old state, r89 counter:** `python3 tools/battery-discrimination-r89.py --battery tools/limine-pin-battery-r89.py --runs 0 --jobs 2 --scratch …` → `verdict met`, `rc=0`; JSON `"runs": []`, `"verdict": "met"`, `"error_rows": 0`. **New state:** `python3 tools/limine-pin-battery-r90.py --gate tools/check-limine-pins.py --runs 0 --work …` → `rc=2`, stdout empty, usage on stderr. |

Notes for the L1:

- This is the class the r89 spot-check routed as §5 item 1 and the r89 lesson left as routed `R89-R1`; it was never
  mined into QUALITY. It is not the "two consecutive rejections from meta-instruments" class: that one is already
  carried by QUALITY 126/129 and named in the r90 declaration ("Two rejections in a row (r88, r89) came from
  meta-instruments …"), so mining it again would duplicate a captured rule.
- Do not re-scope: the fix is an argument-domain check in the instrument, not a change to the r90 predicate, target,
  kill rule or any of the 73 families. The frozen battery bytes already contain it (`8f0daee8…` at `6511437e` and at
  `ce89df93`), so nothing was edited after the freeze.
- The r90 battery refuses `--runs -1` through the same branch; `--runs` absent defaults to 1; `--selftest` is handled
  before the guard, so `--selftest --runs 0` is not a vacuous-count path (it runs the named 5-case selftest).

## QUALITY 130 — draft (live proposal; `corpus/QUALITY.md` ends at 129, line 316)

```markdown
130. **A count that bounds an instrument's evidence is refused before the predicate is evaluated when it empties the
evidence set (R89-EMPTY-RUNS-MET):** when an instrument's verdict quantifies over a list the instrument builds from its
own CLI count (runs, cases, rows, repetitions), any value that yields an empty list — `0`, a negative, or a count the
instrument's usage line excludes — is a usage error: rc 2 and no verdict line, raised before the first fixture is
generated or candidate scored, and never `all()` over an empty sequence; the usage line states the admissible domain
(`--runs N>=1`), and the freeze carries one committed control per refused value showing rc 2 with no verdict line, run
before the first candidate score. Red: round 89's counter accepted `--runs 0`, built zero runs and printed
`verdict met` rc 0 (`7f3f30b3:tools/battery-discrimination-r89.py:275`, `:303`, `:307-308`;
`.ufo/waves/round-89/w1/CriticClaims.md:104-113`), and the r89 battery had the same shape
(`7f3f30b3:tools/limine-pin-battery-r89.py:1112`, `:1128`, `:1135`: rc 0, no output). Green, round 90:
`tools/limine-pin-battery-r90.py:1572` refuses `--runs < 1` with rc 2 before any case runs, and the same bytes are
frozen (`8f0daee8…`, `.ufo/waves/round-90/before/freeze-manifest.sha256:1`); receipts
`.ufo/waves/round-90/w1/ScribeLesson/receipts/`. Not QUALITY 116: 116 refuses a malformed input file, not the count
that bounds the evidence. Not QUALITY 126: 126 judges whether a control's verdict was computed, and zero runs give no
control row to judge. Shown able to fail: the old-state invocation exits 0 (`verdict met` for the counter; no output
for the battery); the new-state invocation exits 2 with no verdict line. Residual, routed: the r90 freeze has no
committed control that invokes the guard — `before/controls/run-controls.sh:22` runs only `--runs 3` — so the guard is
measured here, not regression-controlled; add `K3-runs0-usage` to the next freeze.
Lesson: `corpus/lessons/round-90.md` Mistakes `R89-EMPTY-RUNS-MET`.
```

## Commands run (verbatim; full transcript in `receipts/commands.txt`)

```text
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master
ce89df93e5f576c5c236d4547299e9ea954e8853

$ git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r90/ScribeLesson/lane
$ git -C "$S/lane" rev-parse HEAD
ce89df93e5f576c5c236d4547299e9ea954e8853
$ git -C "$S/lane" rev-parse --show-toplevel
/fast/scratch/hyaku/tsukuroi-r90/ScribeLesson/lane
```

```text
$ cd "$S/lane"
$ python3 tools/limine-pin-battery-r90.py --gate tools/check-limine-pins.py --runs 0 --work "$S/work"
rc=2
stdout: (empty)
stderr:
usage: limine-pin-battery-r90.py [-h] [--gate GATE] [--runs RUNS]
                                 [--work WORK] [--json JSON] [--selftest]
                                 [--reference REFERENCE]
```

```text
$ git show 7f3f30b3:tools/limine-pin-battery-r89.py > "$S/limine-pin-battery-r89.py"
$ sha256sum "$S/limine-pin-battery-r89.py"
3bae11e939cf6900fd29bb24033e6d134de8bf0ae7069cdec3f12f716e8df7f8  /fast/scratch/hyaku/tsukuroi-r90/ScribeLesson/limine-pin-battery-r89.py
$ python3 "$S/limine-pin-battery-r89.py" --gate "$S/lane/tools/check-limine-pins.py" --runs 0 --work "$S/work-old"
rc=0
stdout: (empty)
stderr: (empty)
```

```text
$ git show 7f3f30b3:tools/battery-discrimination-r89.py > "$S/lane/tools/battery-discrimination-r89.py"
$ timeout 120 python3 tools/battery-discrimination-r89.py --battery tools/limine-pin-battery-r89.py --runs 0 --jobs 2 --scratch "$S/counter-work"
rc=0
verdict met
$ timeout 120 python3 tools/battery-discrimination-r89.py --battery tools/limine-pin-battery-r89.py --runs 0 --jobs 2 --scratch "$S/counter-work" --json "$S/old-counter-runs0.json"
rc=0
verdict met
runs=0 verdict=met errors=0
```

```text
$ git -C "$S/lane" show 7f3f30b3:tools/battery-discrimination-r89.py | grep -n 'add_argument("--runs"\|runs = \[run_once\|met = errors\|"met": 0'
275:    ap.add_argument("--runs", type=int, default=3)
303:        runs = [run_once(battery, roster, scratch, a.jobs) for _ in range(a.runs)]
307:    met = errors == 0 and all(r["positives_ok"] == r["positives_total"] and
322:    return {"met": 0, "unmet": 1, "could-not-evaluate": 3}[verdict]

$ git -C "$S/lane" show 7f3f30b3:tools/limine-pin-battery-r89.py | grep -n 'add_argument("--runs"\|runs = \[run_battery\|return 0 if all'
1112:    ap.add_argument("--runs", type=int, default=1)
1128:    runs = [run_battery(gate, work) for _ in range(a.runs)]
1135:    return 0 if all(r["verdict"] == "met" for r in runs) else 1

$ git -C "$S/lane" log --oneline -3 -- tools/battery-discrimination-r89.py
fba764ca round-89: freeze — discrimination counter r89 (opaque launcher, allowlist sandbox + preflight, error rows, manifest void), frozen roster 3 pos / 62 neg with probe receipt, controls K1/F1-F5, host receipt, declaration

$ git -C "$S/lane" log --oneline -3 -- tools/limine-pin-battery-r89.py
81f68d00 round-89: candidate — tools/limine-pin-battery-r89.py (50 families, deterministic CRLF, panic-value lie selftest 15/15), registry rows r89 battery/counter; C2 entry limine-uri-failure-r89 UF1-UF8, SOURCES S361-S363 + S350/S351/S353 anchors, pinned src; README r88 frontier correction (r88 routed 1); dev receipt of the first unmet candidate

$ git -C "$S/lane" diff --stat fba764ca 7f3f30b3 -- tools/battery-discrimination-r89.py
(empty; rc=0)

$ grep -n 'a.runs < 1' tools/limine-pin-battery-r90.py
1572:    if not a.gate or a.runs < 1:

$ grep -n 'Usage: limine-pin-battery-r90' tools/limine-pin-battery-r90.py
112:Usage: limine-pin-battery-r90.py --gate PATH [--runs N>=1] [--work DIR] [--json OUT]

$ sha256sum tools/limine-pin-battery-r90.py
8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5  tools/limine-pin-battery-r90.py
$ git -C "$S/lane" show 6511437e:tools/limine-pin-battery-r90.py | sha256sum
8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5  -

$ grep -n 'limine-pin-battery-r90' .ufo/waves/round-90/before/freeze-manifest.sha256
1:8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5  tools/limine-pin-battery-r90.py

$ grep -n 'runs 3' .ufo/waves/round-90/before/controls/run-controls.sh
22:  ( cd "$w" && python3 "'"$battery"'" --gate "$g" --runs 3 --work "$w" --json "'"$out"'/$n.json" > "'"$out"'/$n.txt" 2>&1; echo "rc=$?" >> "'"$out"'/$n.txt" )
```
