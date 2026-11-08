# ScribeLesson — round 91 w1 report

Seat: ScribeLesson (scribe). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, branch master,
measured at `2d7e09e101996cc1ac5836c6d635f3f608453ac5` (== HEAD at write time), pre-round tip
`40efa4ea2862ab39da02430cada68f6dff230e86`, freeze `d3b0987d68364ccf8b781a755cbcd9563f939468`.
No lane file was edited; no `sudo`, no host write, no git/jj mutation in the lane. All runs were made from
`git clone --shared` at `/fast/scratch/hyaku/tsukuroi-r91/ScribeLesson/fx-qVfSEE/lane` (HEAD `b516d6ae`), then
copied into `.ufo/waves/round-91/w1/ScribeLesson/receipts/`.

## Deliverable

- `.ufo/waves/round-91/w1/ScribeLesson/draft-mistakes.md` — the round-91 lesson `## Mistakes` draft: one row
  (`R91-JUDGE-ORACLE-IMPORTABLE`) in the required `class · evidence pointer · captured-by · fix ·
  shown-able-to-fail` shape, plus the QUALITY draft (numbered **132** — see the conflict note below).
- `.ufo/waves/round-91/w1/ScribeLesson/receipts/` — `commands.txt` (transcript), `r89-counter-oracle.json`,
  `channel-open.json`, `channel-closed.json`, `patch-01-battery-isolate-gate.diff`, `battery-iso-r91.py`
  (the measured isolated battery), `oracle-channel-control.py` (the control that reaches a verdict in both
  channel states), `sibling-oracle-forgery.py` (the forgery that finds the judge as a sibling).

## Verdict per check

| Check | Result |
|---|---|
| Mined mistake from rounds 89-90 not already captured by QUALITY 1-129 (and not by 130/131 either) | **pass** — `R91-JUDGE-ORACLE-IMPORTABLE`; `captured-by: none` |
| Shown able to fail (old state fails, new state passes) | **pass** — old: `82/82 verdict met` rc 0; new (isolated battery): `0/82 verdict unmet` rc 1, 0 error rows; landed gate under the same isolation: `82/82 verdict met` rc 0 |
| QUALITY criterion drafted in house style (bold title with tag, red, green, shown able to fail) | **pass** — criterion 132 drafted; **numbering conflict reported** |
| Seat's two preferred classes | **not mined, with reasons** — `--runs 0` is QUALITY 130 (`R89-EMPTY-RUNS-MET`, landed `b380483e`); "two consecutive rejections from meta-instruments" is named in the r91 declaration (`SCORECARD.md:7619-7621`) and carried by QUALITY 126/129 |
| Lane untouched | **pass** — `git status --porcelain` shows only other seats' wave files; my writes are confined to `.ufo/waves/round-91/w1/ScribeLesson*` |
| Host safety | **pass** — no `sudo`, no write under `/boot`, `/efi`, `/etc`, `/usr`, `/var`; scratch under `/fast/scratch/hyaku/tsukuroi-r91/ScribeLesson` only |

## What was mined and why

**`R91-JUDGE-ORACLE-IMPORTABLE` — a measured claim's subject can import the judge's expected-answer code, so a
subject that reuses the judge is certified `met` while implementing none of the rules.**

The r89 counter's verdict was the battery's own self-report: `7f3f30b3:tools/battery-discrimination-r89.py:238-245`
reads `verdict = j["verdict"]` out of the battery's JSON and maps it to `"met"`. The r89 closure ruled C1 "evidence-verified,
NOT VERIFIED as declared" (`:28`, `:53`): the frozen instrument could not separate the candidate from a forgery. The r90
wave seat built the gate-surface twin (`CriticClaims-7/f2_gate.py:12-13` imports the r90 battery by absolute path) and
the r90 closure routed it (`round-90-verifier-spotcheck.md:132-133`): "name the channel in the docstring or add a control
that kills it". The r91 battery re-opened the channel from the other side: it launches the gate with
`argv = [sys.executable, gate, ...]` (`tools/limine-pin-battery-r91.py:1635`), so for a `tools/`-resident gate
`sys.path[0]` is the battery's own directory and `importlib` reaches the judge. Its "Fixtures carry no answer" sentence
(`:139-141`) names only fixture names/bytes and the conf location; the judge module is not named, and the r91 freeze's 12
controls (`INDEX.tsv`) are all near-miss gates — none imports the judge.

Measured at the tip: `python3 tools/limine-pin-battery-r91.py --gate tools/sibling-oracle-forgery.py --runs 1` →
`families_passed 82/82 verdict met failed -`, **rc 0**. The forgery implements none of R6/R9/R10/V1/U1; it calls the
battery's own `Case.finish()`, `Case.want_unverified()`, `Case.want_on_panic()`, `Case.r8_entries()`. Against the same
battery with the judge module hidden (`bwrap` allowlist + `-I`), the same control reads `0/82 verdict unmet` rc 1 with 0
error rows, while the landed gate still reads `82/82 verdict met` rc 0.

**The class the corpus does not hold.** QUALITY 129 enumerates the channels the *instrument hands the subject*; this is
the subject importing the *judge*. QUALITY 126 governs whether a control reached a verdict (the control here does reach
one — 0 error rows — and the instrument still certifies the subject). QUALITY 41 is about the counter importing the
binder under judgment and about shadow controls. So the class is uncovered; the r90 closure routed the instance without a
criterion behind it, and r91 inherited it.

**Criterion number.** The brief asks for #130; at the tip `corpus/QUALITY.md` already ends at 131 — 130 is
`R89-EMPTY-RUNS-MET` (the r90 lesson's M1, landed `b380483e`) and 131 is `R90-VISIBILITY-WHOLE-FILE`. The draft is
therefore numbered **132**; the L1 decides.

## Findings / limits

1. **The r91 freeze carries no control for this channel.** `INDEX.tsv` lists 12 controls, all near-miss gates;
   `K3-oracle-import` (a gate importing the judge's oracle, expected `unmet`) is the missing one. Not added — lane files
   are read-only to this seat.
2. **The r90 lesson's other residual is also still open.** `R90-R3` routed "`--runs 0` control in the next freeze (QUALITY
   130 residual)"; `.ufo/waves/round-91/before/controls/run-controls.sh:22` still runs only `--runs 3`, and the r91 freeze
   carries no refused-value control either. The refusal itself *is* in the r91 battery (`:1839` `if not a.gate or
   a.runs < 1:` → rc 2), verified at the tip.
3. **The r91 freeze manifest does not pin the r91 battery.** `grep 'limine-pin-battery-r91' .ufo/waves/round-91/before/freeze-manifest.sha256`
   → no match, so the C1 kill rule ("void if the battery bytes … differ from the freeze manifest") cannot fire on the
   instrument. The r91 wave seat `CriticClaims.md` item 8 reports the same fact; I did not re-derive it, I only cite the
   grep.
4. **The isolated battery is a scratch copy, not a lane file.** `receipts/battery-iso-r91.py` differs from the tip battery
   by the one `run_gate` hunk in `receipts/patch-01-battery-isolate-gate.diff`. The closure it demonstrates is specific to
   a `tools/`-resident gate; a lighter closure (`python3 -I` plus a judge copy outside `sys.path`) would need its own
   measurement.
5. **I did not verify the r91 wave's other findings** (`CriticClaims.md` items 1, 2, 3, 6, 7, 10) as lessons — they are
   other seats' rows and outside this seat's scope.

## Commands run

Verbatim transcript with outputs: `.ufo/waves/round-91/w1/ScribeLesson/receipts/commands.txt`. Headlines:

```text
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master
2d7e09e101996cc1ac5836c6d635f3f608453ac5

$ python3 tools/limine-pin-battery-r91.py --gate tools/check-limine-pins.py --runs 0     # in the clone
rc=2   (stdout empty, usage on stderr)

$ python3 "$S/limine-pin-battery-r89.py" --gate tools/check-limine-pins.py --runs 0 --work "$S/wA"   # r89 battery @7f3f30b3
rc=0   (stdout empty, stderr empty)      # vacuous pass

$ python3 tools/battery-discrimination-r89.py --battery tools/limine-pin-battery-r89.py --runs 0 --jobs 4 --scratch "$S"
rc=0   verdict met

$ python3 tools/battery-discrimination-r89.py --battery .ufo/waves/round-89/after/forgeries/usage-oracle.py --runs 3 --jobs 8 --scratch "$S"
rc=0   run 1..3 positives 3/3 negatives 62/62 errors 0 failures -   verdict met
       per-run rows with families_passed==999: [65, 65, 65]   (195 of 195 rows)

$ python3 tools/limine-pin-battery-r91.py --gate tools/sibling-oracle-forgery.py --runs 1 --work "$S/w3"
families_passed 82/82 verdict met failed -      rc=0          # OPEN channel: the judge is importable

$ python3 "$S/battery-iso-r91.py" --gate tools/oracle-channel-control.py --runs 1 --work "$S/w5" --json "$S/channel-closed.json"
families_passed 0/82 verdict unmet failed ALL-PIN-KEYS,…,UNVERIFIED-SORTED   rc=1
channel-closed.json  verdict= unmet  families= 0 / 82  err= 0

$ python3 "$S/battery-iso-r91.py" --gate tools/check-limine-pins.py --runs 1 --work "$S/w2"
families_passed 82/82 verdict met failed -      rc=0          # isolation does not break the real candidate

$ python3 tools/limine-pin-battery-r91.py --gate tools/oracle-channel-control.py --runs 1 --work "$S/w4" --json "$S/channel-open.json"
families_passed 82/82 verdict met failed -      rc=0
channel-open.json   verdict= met  families= 82 / 82  err= 0
```

## Refused / not done

- No lane file was created or modified (the draft and receipts are the only writes; both under
  `.ufo/waves/round-91/w1/ScribeLesson`).
- No `sudo`, no host write, no `/boot`, `/efi`, `/etc`, `/usr`, `/var` write, no `objcopy`/`strip`/`sbsign`/`ukify`/
  `mkinitcpio`/`limine*`/`bootctl`/`efibootmgr`/`pacman`, no sysctl change.
- No git/jj mutation in the lane; the clone was read-only apart from three scratch files I added under the clone's
  `tools/` (the two forgeries and the probe) — all inside `/fast/scratch`, never in the lane.
- No commit, push, publish or deploy.
