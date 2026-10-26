VERDICT: supports

Item C1-F1 — C1 counter frozen, three reruns at the tip, and the impl→tip diff of
`tools/boot-chain-audit.sh`. All three tip runs are identical PASS; the two added lines are one
extra `run_selftest` case (45 → 48 → 49), no production function changed.

## 1. Counter sha256 (frozen identity)

Observed (working tree, lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`):

    $ sha256sum tools/score-bootinputs-r43.py
    886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f  tools/score-bootinputs-r43.py

    $ git cat-file -p fe35700183188f7d712e2932cabde1944efca052:tools/score-bootinputs-r43.py | sha256sum
    886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f  -

Both equal the frozen `886f92c8…e10f`. Same hash also at both tested revisions and at lane HEAD:

    $ for r in 8acf0b02… 717b716a…; do git cat-file -p $r:tools/score-bootinputs-r43.py | sha256sum; done
    8acf0b02 counter_sha=886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f
    717b716a counter_sha=886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f
    $ git rev-parse HEAD:tools/score-bootinputs-r43.py; git hash-object tools/score-bootinputs-r43.py
    fc53583d062475600e3152f05661151d6b3215c0   # HEAD 64646d6e (wave-2 in flight)
    fc53583d062475600e3152f05661151d6b3215c0   # working tree — same blob
    $ git status --porcelain -- tools/score-bootinputs-r43.py tools/boot-chain-audit.sh
    (empty)

Each receipt header independently records `"tool_sha256": "886f92c8…e10f"` with
`"tool_revision": "fe35700183188f7d712e2932cabde1944efca052"`, so the three runs below were
executed by the frozen counter from the freeze commit, in a `--no-local` sandbox clone, not from
the working copy.

## 2. Three runs at the tip (8acf0b022586a0f3164c77659fb96ba5f90949b6)

Command shape (k = 1..3, `TMPDIR=/fast/scratch/hyaku/tsukuroi-r43/C1FinalRerun`):

    python3 tools/run-receipt.py --revision 8acf0b02… --tool-revision fe357001… \
      --out .ufo/waves/round-43/w2/C1FinalRerun/c1-tip-8acf0b0-<k>.jsonl -- \
      tools/score-bootinputs-r43.py --revision '{rev}' \
      --scratch /fast/scratch/hyaku/tsukuroi-r43/C1FinalRerun/s

Receipts: `C1FinalRerun/c1-tip-8acf0b0-1.jsonl`, `-2.jsonl`, `-3.jsonl`.

| field | run 1 | run 2 | run 3 |
|---|---|---|---|
| revision | 8acf0b022586a0f3164c77659fb96ba5f90949b6 | same | same |
| tool_revision | fe35700183188f7d712e2932cabde1944efca052 | same | same |
| cases | 16 | 16 | 16 |
| correct | 16 | 16 | 16 |
| wrong | `[]` | `[]` | `[]` |
| identity | `["1000","1000","1000"]` | same | same |
| identity_ok | 1 | 1 | 1 |
| live | `{"expect":"0","got":"0","rc":0}` | same | same |
| live_agree | 1 | 1 | 1 |
| selftest_line | `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=49 failed=0` | same | same |
| selftest_failures | `[]` | `[]` | `[]` |
| selftest_r43 | 4 | 4 | 4 |
| selftest_pass | 1 | 1 | 1 |
| verdict | **PASS** | **PASS** | **PASS** |
| receipt exit_code / timed_out | 0 / false | 0 / false | 0 / false |
| stderr_tail | `""` | `""` | `""` |
| btime | 1793027300 | 1793027300 | 1793027300 |
| channels_open | `["mount table","uid_map","script path /mnt/bca-lib.sh"]` | same | same |

All six predicate conjuncts hold (`cases==16`, `correct==16`, `identity_ok==1`, `live_agree==1`,
`selftest_pass==1`, `selftest_r43>=2`), so the tip passes the frozen predicate three times out of
three, with no `wrong` entries and no live-host disagreement. Wall time 2.4 s / 3.2 s / 3.0 s
(the 1–3 min figure in the wave brief does not match this counter on this host).

Scratch hygiene: `/fast/scratch/hyaku/tsukuroi-r43/C1FinalRerun/s` is empty after each run
(counter removes what it wrote; `ls -la` shows only `.`/`..`).

## 3. Impl → tip diff of the audited script

    $ git diff --stat 717b716a8943151ace8657e0ca23d7d9b8434f26 8acf0b022586a0f3164c77659fb96ba5f90949b6 -- tools/boot-chain-audit.sh
     tools/boot-chain-audit.sh | 2 ++
     1 file changed, 2 insertions(+)
    $ git diff --name-status 717b716a… 8acf0b02… -- tools/boot-chain-audit.sh
    M	tools/boot-chain-audit.sh

The whole change is two added lines at :1238-1239, inside `run_selftest()` (function starts at
:885 at the tip):

    +    got=$(inputs_newer_than 2000 "$bi/missing" "$bi/old" 2>&1)
    +    st_check 'R43-C1-missing-start-point-silent' 0 "$got"

What changed: one extra selftest case (`R43-C1-missing-start-point-silent`) asserting that
`inputs_newer_than` stays silent — the `2>&1` capture must equal exactly `0`, so any find stderr
text leaking into the result fails the case; it holds because the helper redirects
`find … 2>/dev/null` (tip :470). `inputs_newer_than` (:463-474) and `boot_inputs_newer` (:477-499)
are byte-identical between 717b716 and the tip — the single hunk is the only difference, so the
kill rule ("a function other than `inputs_newer_than`, `boot_inputs_newer`, `run_selftest`
changes") is not tripped, and the round-42 C1 counter / census selftest are untouched by this
file's diff.

Attribution (not the tip commit itself):

    $ git log --oneline -S'missing-start-point-silent' 717b716a…..8acf0b02… -- tools/boot-chain-audit.sh
    9b974f2a round-43: integrate w1 (44 seats) — … R43-C1 stderr selftest case (49) …
    $ git blame -L 1235,1239 8acf0b02… -- tools/boot-chain-audit.sh
    …1238) 9b974f2a … 1239) 9b974f2a
    $ git show --stat --oneline 8acf0b02…
    8acf0b02 round-43: registry row bootinputs-r43 names one tool (REGISTRY-ROW-AMBIGUOUS fix)
     SKILL.md | 2 +-   (1 insertion, 1 deletion)

So the two lines entered at wave-1 integration 9b974f2a, and the tip under test itself only edited a
SKILL.md registry row — it changed nothing in `tools/`.

## 4. Supporting cross-checks (cheap, same fixture clone)

Selftest totals from a `--shared` fixture clone (`fx.k4DR30`, `git rev-parse --show-toplevel` =
that dir, origin removed), script as committed, `TMPDIR` in my scratch:

    6951ead9 => TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=45 failed=0
    717b716a => TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=48 failed=0
    8acf0b02 => TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=49 failed=0

Static case counts agree: `st_check '` = 45 / 48 / 49 and `st_check 'R43-C1-` = 0 / 3 / 4 at
base / impl / tip. This matches the frozen claim "four `R43-C1-*` cases (45 → 49 at
8acf0b0…)" and the counter's `selftest_line`.

Counter at base and impl (same frozen tool-revision, receipts
`C1FinalRerun/c1-base-6951ead.jsonl`, `C1FinalRerun/c1-impl-717b716.jsonl`):

- 6951ead90566b2d74f7c45b4efca29246badad64: cases 16, **correct 8**, verdict FAIL, exit 1. All 8
  `wrong` entries are `expect 1 / got 0 / rc 0` — `miss/etc/fstab-newer`, `miss/etc/crypttab-newer`,
  `miss/etc/mkinitcpio.conf-newer`, `miss/etc/mkinitcpio.conf.d-newer`, `miss/etc/default/limine-newer`,
  `miss/etc/limine-snapper-sync.conf-newer`, `multi-miss-deep-modules-newer`,
  `unreadable-dir-modules-newer` — i.e. exactly the fail-open arm the fix targets.
- 717b716a8943151ace8657e0ca23d7d9b8434f26: cases 16, correct 16, wrong `[]`, identity_ok 1,
  live_agree 1, selftest `PASS total=48 failed=0`, selftest_r43 3, verdict PASS, exit 0.

Base FAIL → impl PASS → tip PASS (3/3) reproduces the declared discrimination with the frozen
counter, and the counter is unchanged across all three revisions.

## 5. Observations / risks

- Declaration wording: `SCORECARD.md:2661` (C1 row, unchanged at the tip) still says "three
  `R43-C1` selftest cases (45 → 48)". The tip has four cases (total 49) because wave-1 integration
  9b974f2a added `R43-C1-missing-start-point-silent`. The counter only requires
  `selftest_r43 >= 2`, so neither FAILs, but the row's count is one behind the tip.
- The added case guards stderr silence, not the masking arm: at base the same construction
  (`missing` start point plus an old input) already printed `0`, so this case alone would also pass
  at base; the masking discrimination comes from the other three `R43-C1-` cases and the counter's
  16-case leg. It is a regression guard, not a new falsifier.
- Lane HEAD during my runs was 64646d6e (master, wave-2 in flight), not the tip under test;
  `run-receipt.py` clones the lane at `--revision`/`--tool-revision`, so the receipts describe
  8acf0b0 / fe357001 content regardless — no read of wave-2 working-tree edits is implied.
- Not done (out of this item): no mount-table-gated control-battery run, no namespace-channel
  closure work, no review of the C2 knowledge file. Those belong to other seats.
- Host guard: read-only on the lane (git read commands only, plus receipt writes to my own seat
  dir); fixture clone and all scratch under `/fast/scratch/hyaku/tsukuroi-r43/C1FinalRerun`;
  no `/tmp` path used as evidence; no packages installed or upgraded (nothing needed), no pacman
  transaction, no service or sysfs change, no btrfs command. Scratch removed after receipts were
  copied into the seat dir.

## 6. Evidence paths

- `C1FinalRerun/c1-tip-8acf0b0-1.jsonl`, `-2.jsonl`, `-3.jsonl` (tip, three runs, PASS)
- `C1FinalRerun/c1-base-6951ead.jsonl` (base, FAIL, correct 8)
- `C1FinalRerun/c1-impl-717b716.jsonl` (impl, PASS, selftest 48)
