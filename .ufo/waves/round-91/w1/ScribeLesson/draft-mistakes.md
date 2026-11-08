# Draft — round-91 lesson `## Mistakes` (seat ScribeLesson)

Measured at lane revision `2d7e09e101996cc1ac5836c6d635f3f608453ac5` (`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`), pre-round tip `40efa4ea2862ab39da02430cada68f6dff230e86`, freeze `d3b0987d68364ccf8b781a755cbcd9563f939468`. Every execution was made from a `git clone --shared` at `/fast/scratch/hyaku/tsukuroi-r91/ScribeLesson/fx-qVfSEE/lane` (HEAD `b516d6ae`); the lane was not written, no `sudo`, no host write, no git/jj mutation in the lane. Raw receipts: `.ufo/waves/round-91/w1/ScribeLesson/receipts/` (`commands.txt`, `r89-counter-oracle.json`, `channel-open.json`, `channel-closed.json`, `patch-01-battery-isolate-gate.diff`, `battery-iso-r91.py`, `oracle-channel-control.py`, `sibling-oracle-forgery.py`).

Row shape: `class · evidence pointer · captured-by · fix · shown-able-to-fail`.

## The row

| Class | Evidence pointer | Captured-by | Fix | Shown able to fail |
|---|---|---|---|---|
| **M1 — `R91-JUDGE-ORACLE-IMPORTABLE`**: a measured claim's judge can be imported by the subject it judges, so a subject that reuses the judge's own expected-answer code is certified `met` while implementing none of the rules. The r89 counter read the battery's own `verdict` field out of the battery's JSON and mapped it to its own verdict (`j["verdict"]` → `"met"`), and the r90 closure routed the same shape one level down — a gate importing the r90 battery's `Case.finish`/`want_on_panic` reads 73/73 — but the r91 instrument re-opened it: the r91 battery computes the expectation inside the same `tools/` directory the gate is launched from, so `sys.path[0]` of the gate is the battery's own directory. | `7f3f30b3:tools/battery-discrimination-r89.py:238-245` (`verdict = j["verdict"]` read out of the battery's own JSON receipt; `:243` `return "met", fp`; the counter's verdict IS the battery's self-report); `c0f91856:corpus/lessons/round-89-verifier-spotcheck.md:28` and `:53` (r89 closure: "evidence-verified, NOT VERIFIED as declared" — "the frozen instrument cannot separate the candidate from a forgery, so C1 does not verify as declared"); `b1ef413d:.ufo/waves/round-90/w1/CriticClaims.md:20-27` (the r90 wave seat's oracle-import gate; `CriticClaims-7/f2_gate.py:12-13` `BATT = ".../tools/limine-pin-battery-r90.py"` + `spec_from_file_location`); `40efa4ea:corpus/lessons/round-90-verifier-spotcheck.md:132-133` (r90 closure routing it: "name the channel in the docstring or add a control that kills it"); `2d7e09e1:tools/limine-pin-battery-r91.py:1635` (`argv = [sys.executable, gate, ...]` — the gate runs with `sys.path[0]` = the gate's own directory, which for a `tools/`-resident gate IS the battery's directory, so `importlib` reaches the judge) and `:139-141` (the battery's "Fixtures carry no answer" sentence, which names only fixture names/bytes and the conf location — the judge module itself is not named); `2d7e09e1:SCORECARD.md:7612-7643` (the r91 declaration's C1 row: no limits paragraph names the oracle channel, and the 12 committed controls `K1,K2,N01-N10` are all near-miss gates — no control imports the battery) | `none` — QUALITY 126 (`R88-CONTROL-PASSED-BY-CRASH`) judges whether a control's verdict was computed and in every layout; QUALITY 129 (`R89-NAME-CHANNEL-UNCONTROLLED`) enumerates the channels the *instrument hands the subject* (files it can read, argv, stdout/stderr, environment, `/proc`, timing) — it does not cover the subject importing the *judge's* oracle module; QUALITY 41 (`R20-C2-ORACLE`) is about the counter importing the binder under judgment and about shadow controls, not a gate importing its battery. The r90 closure itself routed the channel under "name the channel in the docstring or add a control that kills it" without landing a criterion for it, so it recurred in r91. | Close the channel in the instrument and bind it with a control: the battery must run the gate in a namespace that does not contain the battery module, and the freeze must carry one committed control that imports the judge's oracle and must read `unmet`. Proposed patch (not applied; lane files are read-only to this seat): `.ufo/waves/round-91/w1/ScribeLesson/receipts/patch-01-battery-isolate-gate.diff` — a `bwrap` allowlist (`/usr`, `/etc`, `/dev`, `/proc`, tmpfs `/tmp`, the gate file read-only, the case directory) around the gate launch, `-I` so `sys.path[0]` is not the gate's directory. Plus the channel named in the battery's "Fixtures carry no answer" sentence, and a `K3-oracle-import` control in the next freeze. | **Old state (open channel) — FAILS.** `python3 tools/limine-pin-battery-r91.py --gate tools/sibling-oracle-forgery.py --runs 1` (the forgery finds the battery as a *sibling* of the gate, so it needs no hardcoded path) → `families_passed 82/82 verdict met failed -`, **rc 0**. The gate implements none of R6/R9/R10/V1/U1: it calls the battery's own `Case.finish()`, `Case.want_unverified()`, `Case.want_on_panic()` and `Case.r8_entries()`. With the same battery and a channel control that falls back to a deliberately wrong answer when the import fails (`receipts/oracle-channel-control.py`) → `families_passed 82/82 verdict met`, rc 0. **New state (closed channel) — PASSES.** The same control against the isolated battery (`receipts/battery-iso-r91.py`) → `families_passed 0/82 verdict unmet`, **rc 1**, 0 error rows (the control reached a verdict, not a crash — QUALITY 126(a) satisfied), and the landed gate under the same isolated battery → `families_passed 82/82 verdict met`, rc 0 (the isolation does not break the real candidate). |

## Why this class and not the two the seat named

The seat brief preferred (a) "an instrument's CLI accepts a degenerate argument that makes the verdict vacuous" and (b) "two consecutive rejections from meta-instruments judging instruments (r88, r89)". Both are already carried:

- **(a) is QUALITY 130** (`R89-EMPTY-RUNS-MET`), landed at `b380483e` — the r90 lesson's M1. The r91 instrument already carries the fix: `tools/limine-pin-battery-r91.py:1839` `if not a.gate or a.runs < 1: ap.print_usage(...); return 2`, raised before any fixture is built. Verified at the tip: `python3 tools/limine-pin-battery-r91.py --gate tools/check-limine-pins.py --runs 0` → **rc 2**, stdout empty, usage on stderr; the old r89 battery at `7f3f30b3` → **rc 0**, stdout empty, stderr empty (vacuous pass); the r89 counter at `7f3f30b3` → `verdict met`, **rc 0** with `"runs": []`. Re-mining (a) would duplicate QUALITY 130 and the r90 lesson's M1 verbatim; the criterion and its fix are already in the corpus.
- **(b) is already named in the r91 declaration itself** (`SCORECORD.md:7619-7621`: "the last three rejected closures (r88, r89, r90) ... The two rejections in a row came from meta-instruments (a counter judging a battery, then a battery that cannot tell an independent implementation from one that imports the oracle)") and is carried by QUALITY 126/129. Mining (b) would restate a rule the corpus already has.

M1 is the class those two leave open: **the direction of the channel is the other way round.** QUALITY 129 enumerates what the *instrument hands the subject*; M1 is the subject importing the *judge's* oracle. Both the r89 counter (which read the battery's own `verdict` field) and the r90/r91 batteries (whose `Case` oracle sits in the gate's `sys.path[0]`) fail on that direction, and no criterion names it. This is the same defect the r90 closure routed at `round-90-verifier-spotcheck.md:132` and that the r91 freeze did not discharge: the r91 controls are 12 near-miss gates, none of which imports the judge.

## QUALITY 132 — draft (live proposal; `corpus/QUALITY.md` ends at 131, line 321)

**Numbering conflict with the seat brief (the L1 decides).** The brief asks for "one QUALITY criterion (number 130)". At the lane tip `2d7e09e1` `corpus/QUALITY.md` already ends at **131**: criterion **130** is `R89-EMPTY-RUNS-MET` (landed `b380483e`, the r90 lesson's M1) and criterion **131** is `R90-VISIBILITY-WHOLE-FILE` (same commit). Re-using 130 would collide with `R89-EMPTY-RUNS-MET`; I therefore draft the new criterion as **132** (the next free number) and leave the number to the L1. The content is the un-captured class M1, not a re-statement of 130 or 131.

```markdown
132. **A measured claim's subject cannot import the judge's expected-answer code, and the channel is named and controlled (R91-JUDGE-ORACLE-IMPORTABLE):** when a claim's instrument judges a subject by running it, the instrument's own expected-answer code (its oracle, its `Case`/fixture model, its rule tables) must be unreachable from the subject's process — the subject runs in a namespace or interpreter whose module search path does not contain the judge — and the instrument's verdict must be its own computation, never a field the subject wrote or a value the subject obtained from the judge; the instrument's anti-oracle sentence enumerates every such channel, and the freeze carries one committed control per channel that reaches the target through it and must read `unmet` in every layout the counting command permits (QUALITY 126 a/b apply). A judge that reads the subject's own `verdict` field, or a subject that can `import` the judge's oracle and call its own `finish`/`want_*` helpers, measures agreement with the judge, not the subject's behaviour. Red: the round-89 counter read the battery's own verdict field and certified a battery that implemented no rule (`7f3f30b3:tools/battery-discrimination-r89.py:238-245`; the committed name oracle read 65/65 hits and `verdict met` rc 0 in each of three runs, `.ufo/waves/round-89/after/forgeries/usage-oracle.receipt.txt`); the round-90 closure routed the same shape for the gate surface ("a gate importing the battery's own `Case.finish`/`want_on_panic` reads 73/73; name the channel in the docstring or add a control that kills it", `corpus/lessons/round-90-verifier-spotcheck.md:132-133`), and the round-91 battery re-opened it — the gate is launched from the judge's own directory, so `sys.path[0]` reaches the battery module: a gate that finds the battery as a sibling and calls its `Case.finish`/`want_unverified`/`want_on_panic` reads `families_passed 82/82 verdict met` rc 0 on the frozen r91 battery (`tools/limine-pin-battery-r91.py:1635`, `:139-141`; receipts `.ufo/waves/round-91/w1/ScribeLesson/receipts/`). Green, round-92 proposal: the battery launches the gate under a `bwrap` allowlist that does not contain the battery module and with `-I`, so `sys.path[0]` is not the gate's directory; the same oracle-import control then reads `0/82 verdict unmet` rc 1 with 0 error rows while the landed gate still reads `82/82 verdict met` rc 0 (`.ufo/waves/round-91/w1/ScribeLesson/receipts/patch-01-battery-isolate-gate.diff`). Not QUALITY 129: 129 enumerates the channels the instrument hands the subject; this is the subject importing the judge. Not QUALITY 126: 126 governs whether a control reached a verdict; here the control reaches a verdict and the instrument still certifies the subject. Not QUALITY 41: 41 is about the counter importing the binder under judgment and about shadow controls. Lesson: `corpus/lessons/round-91.md` Mistakes `R91-JUDGE-ORACLE-IMPORTABLE`.
```

## Notes for the L1

- **Do not re-scope.** The fix is a channel closure in the *instrument* (the battery's launch of the gate) plus a committed control; it does not touch C1's predicate, target, kill rule, the 82 families, or the r91 gate's V1/U1 repair. The r91 C1 claim as measured (`82/82 ×3` canonical and clone) is unaffected by the defect — the defect is that the number cannot distinguish an independent implementation from one that reuses the judge.
- **The r91 freeze does not contain this channel's control.** `INDEX.tsv` lists 12 controls, all near-miss gates; `K3-oracle-import` (a gate that imports the judge's oracle and must read `unmet`) is the missing one. The r90 lesson routed "`--runs 0` control in the next freeze (QUALITY 130 residual)" (R90-R3) — also absent from the r91 freeze; `run-controls.sh:22` still runs only `--runs 3`. Both are the L1's call; this seat changed no lane file.
- **Adjacent findings I did not mine** (they belong to other seats' rows, and I did not verify them as lessons): the r91 wave's `CriticClaims.md` items 1, 2, 3, 6, 7, 8, 10 are separate defects (declaration literal counts, a broken K2 control, an unsorted-list forgery, N01/N10 byte-identity, a clause map, a freeze-manifest that omits the battery, and working-tree gate drift). My row M1 is the one class neither QUALITY nor the r91 wave already owns: the judge-oracle import channel.
- **A caveat on the green leg.** The isolated battery I measured is a scratch copy under `/fast/scratch`, not a lane file. It closes the channel for a `tools/`-resident gate because the allowlist binds only the gate file and the case directory. If the L1 prefers a lighter closure (e.g. `python3 -I` plus a copied battery outside `sys.path`), the control's expected reading stays `unmet` and the landed gate stays `met` — but the specific argv in the patch is the one I measured.

## Commands run (verbatim; full transcript in `receipts/commands.txt`)

```text
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master
2d7e09e101996cc1ac5836c6d635f3f608453ac5

$ git clone --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin $S/fx-qVfSEE/lane
$ git -C "$S/fx-qVfSEE/lane" rev-parse HEAD
b516d6ae13ec0bba3ef89589ac1cac86f73a9632
```

```text
$ cd "$S/fx-qVfSEE/lane"

$ python3 tools/limine-pin-battery-r91.py --gate tools/check-limine-pins.py --runs 0
rc=2
stdout: (empty)
stderr:
usage: limine-pin-battery-r91.py [-h] [--gate GATE] [--runs RUNS]
                                 [--work WORK] [--json JSON] [--selftest]
                                 [--reference REFERENCE]
```

```text
$ git show 7f3f30b3:tools/limine-pin-battery-r89.py > "$S/limine-pin-battery-r89.py"
$ sha256sum "$S/limine-pin-battery-r89.py"
3bae11e939cf6900fd29bb24033e6d134de8bf0ae7069ddec3f12f716e8df7f8  (r89 battery, frozen digest 3bae11e9… as in the r89 spot-check)
$ python3 "$S/limine-pin-battery-r89.py" --gate tools/check-limine-pins.py --runs 0 --work "$S/wA"
rc=0
stdout: (empty)
stderr: (empty)
```

```text
$ python3 tools/battery-discrimination-r89.py --battery tools/limine-pin-battery-r89.py --runs 0 --jobs 4 --scratch "$S" --json "$S/r89-counter-runs0.json"
rc=0
verdict met
```

```text
$ python3 tools/battery-discrimination-r89.py --battery .ufo/waves/round-89/after/forgeries/usage-oracle.py --runs 3 --jobs 8 --scratch "$S" --json "$S/r89-counter-oracle.json"
rc=0
run 1 positives 3/3 negatives 62/62 errors 0 failures -
run 2 positives 3/3 negatives 62/62 errors 0 failures -
run 3 positives 3/3 negatives 62/62 errors 0 failures -
verdict met
$ python3 -c "...count rows with families_passed==999..."
hits999: 195 of 195
per-run hits999: [65, 65, 65]
verdict: met error_rows: 0
```

```text
$ python3 tools/limine-pin-battery-r91.py --gate tools/sibling-oracle-forgery.py --runs 1 --work "$S/w3"
families_passed 82/82 verdict met failed -
rc=0
```

```text
$ python3 "$S/battery-iso-r91.py" --gate tools/oracle-channel-control.py --runs 1 --work "$S/w5" --json "$S/channel-closed.json"
families_passed 0/82 verdict unmet failed ALL-PIN-KEYS,BAD-OVER-UNRESOLVED,…,UNVERIFIED-SORTED
rc=1
$ python3 -c "…verdict, families, error rows…"
channel-closed.json verdict= unmet families= 0 / 82 err= 0
```

```text
$ python3 "$S/battery-iso-r91.py" --gate tools/check-limine-pins.py --runs 1 --work "$S/w2"
families_passed 82/82 verdict met failed -
rc=0
```

```text
$ python3 tools/limine-pin-battery-r91.py --gate tools/oracle-channel-control.py --runs 1 --work "$S/w4" --json "$S/channel-open.json"
families_passed 82/82 verdict met failed -
rc=0
$ python3 -c "…verdict, families, error rows…"
channel-open.json verdict= met families= 82 / 82 err= 0
```

```text
$ git -C "$S/fx-qVfSEE/lane" show 7f3f30b3:tools/battery-discrimination-r89.py | sed -n '238p;243p'
            verdict = j["verdict"]
            return "met", fp

$ grep -n 'argv = \[sys.executable, gate' tools/limine-pin-battery-r91.py
1635:    argv = [sys.executable, gate, "--conf", conf, "--esp", esp]

$ grep -n 'a.runs < 1' tools/limine-pin-battery-r91.py
1839:    if not a.gate or a.runs < 1:

$ git -C "$S/fx-qVfSEE/lane" log --oneline -3 -- tools/battery-discrimination-r89.py
fba764ca round-89: freeze — discrimination counter r89 (opaque launcher, allowlist sandbox + preflight, error rows, manifest void), frozen roster 3 pos / 62 neg with probe receipt, controls K1/F1-F5, host receipt, declaration
$ git -C "$S/fx-qVfSEE/lane" log --oneline -3 -- tools/limine-pin-battery-r91.py
1652b086 round-91: strengthen UNVERIFIED-SORTED family, fix u1_ok sorted check, N08 reverse patch
d3b0987d round-91: freeze declaration, battery r91, candidate gate draft, controls
$ git -C "$S/fx-qVfSEE/lane" log --oneline -3 -- corpus/lessons/round-90-verifier-spotcheck.md
40efa4ea round-90 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git -C "$S/fx-qVfSEE/lane" log --oneline -3 -- corpus/lessons/round-89-verifier-spotcheck.md
c0f91856 round-89 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git -C "$S/fx-qVfSEE/lane" log --oneline -3 -- .ufo/waves/round-90/w1/CriticClaims.md
b1ef413d round-90: integration after WAVE-DONE — TV1/TV2/TV4 … (wave w1 evidence, results, lesson draft)
```

```text
$ grep -n 'limine-pin-battery-r91' .ufo/waves/round-91/before/freeze-manifest.sha256
(no match — the frozen manifest does not pin the r91 battery itself)
$ cat .ufo/waves/round-91/before/controls/gates/INDEX.tsv | cut -f1
name
K1-landed-gate
K2-landed-adapter
N01-panic-whole-file
N02-measured-whole-file
N03-no-first-line-exception
N04-first-line-inverted
N05-no-unverified-field
N06-unverified-includes-pins
N07-unverified-non-efi
N08-unverified-unsorted
N09-unverified-last-path
N10-panic-first-anywhere
(no oracle-import control)
```
