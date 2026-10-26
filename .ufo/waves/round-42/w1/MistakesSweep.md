VERDICT: defect-found

# M-1 — mistakes mined for `corpus/lessons/round-42.md` `## Mistakes`

seat `MistakesSweep-2`, round 42 w1, 2026-10-26. Scratch `/fast/scratch/hyaku/tsukuroi-r42/MistakesSweep-2/`
(removed on exit; nothing was built outside it). Receipts: `.ufo/waves/round-42/w1/MistakesSweep-2/receipts.txt`
(7933 B; every command and its output quoted below is in that file). No counter and no census selftest was run —
the host is shared and the wave runs one counter at a time; every claim below rests on committed bytes, the
committed receipts, or file metadata, and §4 names what was not run.

Read: `corpus/lessons/round-41-verifier-spotcheck.md` (§3 axis verdicts, §6 routed defects), `corpus/lessons/round-41.md`
`## Mistakes` (class vocabulary in use), `SCORECARD.md:2560-2575` ("Round 42 — declaration", rows C1/C2 and the
control battery text), `corpus/lessons/round-42.md` (the file under construction), `.ufo/waves/round-42/controls/`
(2 runners, 15 control receipts, 2 summaries), `.ufo/waves/round-42/before/` (2 before receipts + 2 registry runs),
`.ufo/waves/round-42/impl/c1-able-to-fail.txt`, both frozen counters, the base and implementation census bytes,
`git -C … log --stat c8efaa3f..f50c28d` (3 commits: declaration+freeze, implementation, C2 entry).

Candidate rows, most severe first. Paths are relative to the lane root. Class vocabulary as routed: vacuous,
survivor, stale-premise, reference-drift, number-drift, scope, attribution, landing, provider.

## 1. Proposed rows

| ID | Class | Evidence pointer | Captured-by | Fix, and how it is shown able to fail |
|---|---|---|---|---|
| R42-C1-SELFTEST-UNMEASURED | vacuous | The C1 surface promises "adds a selftest case carrying a large error-bearing `-Qkk` sample" (`SCORECARD.md:2573`), but the frozen predicate holds no selftest-content conjunct (`tools/score-size-invariance-r42.py:43`, `:360-365`: `selftest_pass` is only "exit 0 and `FAIL` count 0"), and it is already `1` at the base (`before/c1-before.jsonl` line 2: `PASS (128 cases, 128 passed, 0 failed)`). The battery's own reachability control is the counterexample: `controls/C1-K6.jsonl` = `PASS`, `selftest_label "PASS (128 cases, 128 passed, 0 failed)"`, while `run_controls_c1.py:variant('K6')` is the base census plus the probe fixes only — reconstructing it beside `git show 4476620:tools/tsukuroi-census.sh` gives 125 vs 127 `check` calls and `R42-C1` count 0 vs 2, diff = 25 added lines (3 comments + the two case blocks) | none — QUALITY 88 requires a must-PASS battery member but no criterion says the accepted member must be the shipped candidate, and the declaration's target sentence does not repeat the selftest deliverable | Round 43 counter gains `selftest_cases >= 130` (parsed from the same badge) and `census.count('(R42-C1)') == 2`; K6 is renamed "fix-only surrogate" and a new reachability control runs the implementation bytes. Shown able to fail: re-score the two committed controls with the tightened counter — `C1-K6` must flip to FAIL (`128 cases`, `0` labels) while `git show 4476620:…` PASSes and the base FAILs on the same conjunct (128). Also commit the hybrid builder behind `impl/c1-able-to-fail.txt`: its implementation digest is re-derivable (`sha256 = 46d62a24…`, checked), its hybrid digest `a8fbfd51…` is not — no hybrid file or script is committed |
| R42-C1-P6-NOT-NEUTRAL | stale-premise | The counter states every twin pair "differ only by verdict-neutral padding lines (lines no packages/update-safety parser rule matches)" (`tools/score-size-invariance-r42.py:10`) and the declaration repeats "1 MiB of verdict-neutral, marker-free padding" (`SCORECARD.md:2573`). P6's padding is `err_pad` (`:153-158`, used at `:198`) = `error: … (Permission denied)` lines, and the base census's own rules match every one: `^error:` at `tools/tsukuroi-census.sh:692` and the `nonroot` counter at `:702-703` (`\(failed to calculate SHA256 checksum\)\|\(Permission denied\)`). The receipt shows the consequence: `controls/C1-K5.jsonl` P6 large line reads `PLANE packages: HEALTHY (… nonroot_artifacts=11606; …)` while the small twin's line does not. The oracle is therefore only satisfiable on P6 by a census that returns early on the first error — an unstated behavioural requirement, not size invariance | none — fixtures are frozen before a seat reads them, and no criterion tests the neutrality claim itself | Add a counter self-check over the padding generators: feed `qkk_pad`/`err_pad` output to the census's own rules and require no match; relabel P6 ("error storm, first error decides — not neutral padding") or give it `qkk_pad` and keep a storm case of its own; add a case whose signal is *two* error lines with neutral padding so a "keep only the first error" filter is caught. Shown able to fail: the self-check is red over `err_pad` (matches `^error:` and `Permission denied`) and green over `qkk_pad` today — a second-scale demonstration, no census run |
| R42-C1-K5-OVERDETERMINED | survivor | `controls/C1-K5.jsonl`: `FAIL` with `selftest_label "FAIL (128 cases, 127 passed, 1 failed)"` **and** `non_invariant ["P6"]`, `invariant 9`. The declared "padding-filter mirror evasion" (declaration battery text) is invariant on 9 of 10 twins (P1-P5, U1-U4): only the non-neutral P6 twin kills it, and the control fails on an unrelated conjunct at the same time, so the receipt cannot show which check did the killing — the same shape as round-40 `R40-CONTROL-OWN-BASELINE` | QUALITY 88 ("violates exactly one named parameter") — applied to counters, not to the pre-data controls | Make K5 filter only when `[ "${#s_out}" -gt 65536 ]` (small fixtures and the selftest stay byte-identical), then re-score. Shown able to fail: the re-run receipt must read `selftest_pass 1` and `non_invariant ["P6"]`; a reading of `127/128` shows the control is mis-built, and `invariant 10` shows the oracle has no kill for this family. One runner pass with `--names K5` |
| R42-BATTERY-SUMMARY-COLLISION | landing | Both runners open the same path: `controls/run_controls_c1.py:167` and `run_controls_c2.py:152` write `os.path.join(a.out,'battery-summary.jsonl')`. The directory holds no `battery-summary.jsonl`; it holds `battery-summary-c1.jsonl` (birth `16:36:59`, 50 s after the last C1 control `C1-K8.jsonl` `16:36:09`) and `battery-summary-c2.jsonl` (birth `16:30:49`, 46 s after the last C2 control `C2-K5.jsonl` `16:30:03`, i.e. 5 s after the C1 run started `16:30:44`) — `stat --format=%w`; neither name is producible by either runner, so both are copies made after their runs, and the runner's own `battery-summary.jsonl` was never kept. Neither summary, nor any of the 15 per-control receipts, is in the tree at the dispatch tip: `git ls-tree -r f50c28d -- .ufo/waves/round-42/controls` lists the two scripts only | none — no criterion asks a pre-data battery's summary to be the runner's own output, or the receipts to be committed before the declaration points at them | Suffix the summary by battery in the runners, give each battery its own `--out`, tee stdout to a per-battery log, and commit all receipts in the integration commit. Shown able to fail: `grep -c battery-summary.jsonl` over the two runners is 2 today and must be 0 after; a check comparing `git ls-tree` with the declared directory is red today (2 tracked files vs 17 JSONL artifacts on disk) and green after the commit — the content of both copies agrees with their per-control receipts, so only provenance is lost, not value |
| R42-FREEZE-CENSUS-LIVE-PATH | reference-drift | `before/sources-census-start.txt:1` is a header naming base `c8efaa3f`, the `git archive` export and the run time; `before/sources-census-at-freeze-a84fc9de.txt` has no header and its last line is `tsukuroi ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md` — the live lane, not an export of `a84fc9de`. The two files differ only in that path and the header (43 vs 42 lines; 40 W04 each), so the receipt named for the freeze commit does not name the revision it read, and `corpus/lessons/round-42.md` "Sources census" calling it "the same command at the freeze commit" is a claim the bytes do not carry | none — R41-BASE-MISREAD's fix covers what counters name, not what path a registry run reads | Re-run on a `git archive a84fc9de` export with the start receipt's header, or drop the file and say the registry was read from the working tree at freeze time. Shown able to fail: a check that reads line 1 for the revision and requires the `ok` path to resolve under the export directory is red on today's file and green on a re-run export |
| R42-C1-CLASS-UNSWEPT | scope | The rule the fix follows is written as a comment inside `probe_packages` (`tools/tsukuroi-census.sh:692-695`, implementation), but the construct remains at 12 sites in the same file — `:676,:798,:931,:963,:969,:1051,:1162,:1426,:1483,:1497,:1501,:1783` — five of them bare assignments (`:931` `$CAP_OUT\|head -n1`, `:969`, `:1051` nvidia-smi, `:1426`, `:1501`), where a probe that ever printed more than the pipe buffer would kill the census exactly as `:1652` did. No exposure today: those probes are `systemctl`/`nvidia-smi` one-liners, and the rest sit in process substitutions or carry `\|\| true` (grep count 26 base → 24 impl) | QUALITY 82 ("fix the class, not the case") — the declaration scopes the claim to two planes, so this is residue, not a false claim | Move the rule to the `cap()` helper's comment and add a lint gate over the census bytes (no `printf … \| (head\|grep -q\|grep -m1)` outside `run_selftest`). Shown able to fail: the gate reports 12 impl sites today (18 at the base, 6 of them the fixed ones) and 0 after the sweep — no census run |
| R42-C1-SCRATCH-FALLBACK-TMP | landing | `tools/score-size-invariance-r42.py:300-303`: `parent = a.scratch or os.environ.get('TMPDIR') or None`, then `tempfile.mkdtemp(…, dir=parent)`. On this host `TMPDIR` is unset (`env -u TMPDIR python3 -c 'import tempfile;print(tempfile.gettempdir())'` → `/tmp`), so a caller who omits `--scratch` builds the 1 MiB fixtures and both census runs under `/tmp` — the w1 seat rules' Scratch bullet ("Never build under `/tmp`") and the R40-TMP-MISROOT / R41-TMP-MISROOT-REPEAT class; the docstring's "(never a hardcoded /tmp)" (`:49`) states the opposite of the behaviour | the w1 seat rules' Scratch bullet and R40-TMP-MISROOT; the frozen counter honours `TMPDIR` but neither requires it nor refuses the fallback | Require one of `--scratch`/`TMPDIR` and exit 2 (already reserved for usage) otherwise. Shown able to fail: with `TMPDIR` unset the declaration's command, minus `--scratch`, reaches `tempfile.gettempdir()` `/tmp` today; after the fix it exits 2 and creates nothing. I did not run the counter to watch the `/tmp` directory appear — that would itself be the violation |

## 2. Evidence detail (what each row rests on)

- **R42-C1-SELFTEST-UNMEASURED.** `python3 -c` importing `run_controls_c1.py` and calling `variant('K6', base)`, compared
  with `git show 4476620:tools/tsukuroi-census.sh`: `k6 check calls 125 | impl check calls 127`, `k6 R42-C1 0 | impl R42-C1 2`,
  hunk headers `@@ -691,0 +692,3 @@`, `@@ -2346,0 +2350,10 @@`, `@@ -2541,0 +2555,12 @@` (receipts.txt §C). The committed
  receipt `controls/C1-K6.jsonl` independently records `PASS` with the 128-case badge (`§D`). Consequence: at the tip the
  predicate would pass a census identical to `4476620` minus both `R42-C1` cases. The round did show those cases red on the
  base probes (`impl/c1-able-to-fail.txt`: hybrid run exit 1, `FAIL (130 cases, 128 passed, 2 failed)`; implementation
  `PASS (130 cases, 130 passed, 0 failed)`), so the deliverable is real — it is the oracle that cannot see it.
- **R42-C1-P6-NOT-NEUTRAL.** `err_pad` emits `error: {pkg}: /usr/… (Permission denied)` and the census counts that text in
  `nonroot` (`tools/tsukuroi-census.sh:702-703`); the K5 large line carries `nonroot_artifacts=11606` (receipts.txt §F).
  The other padding generator, `qkk_pad` (`:138-151`), emits `warning: … (Modification time mismatch|Size mismatch|…)` and
  `N total files, 0 altered files`, which none of those rules match — so nine pairs are genuinely neutral and P6 is not.
- **R42-C1-K5-OVERDETERMINED.** `controls/C1-K5.jsonl`: `verdict FAIL | invariant 9 | non_invariant ["P6"] | selftest_pass 0 |
  label TSUKUROI_CENSUS_SELFTEST: FAIL (128 cases, 127 passed, 1 failed)` (receipts.txt §D). K1/K2/K3/K4, by contrast, each show
  `selftest_pass 1`, so their FAIL is attributable; K5 is the only degenerate control.
- **R42-BATTERY-SUMMARY-COLLISION.** `grep -n battery-summary.jsonl` → `run_controls_c1.py:167`, `run_controls_c2.py:152`;
  `stat --format='%n birth=%w'` on the four files (§A); `ls controls/battery-summary.jsonl` → No such file;
  `git ls-tree -r f50c28d -- …/controls` → two scripts. Summary contents agree with the per-control receipts
  (`battery-summary-c1.jsonl`: K0-K5/K7/K8 FAIL, K6 PASS; `-c2`: K0-K2/K4/K5 FAIL, K3 PASS), i.e. the copies are faithful.
- **R42-FREEZE-CENSUS-LIVE-PATH.** `diff` of the two receipts with paths normalised prints one deleted line (the start
  header) and nothing else; tail of the freeze receipt is the live-lane `ok` path (§G).
- **R42-C1-CLASS-UNSWEPT.** `grep -nE '^ *[a-z_]+=\$\(printf .*\| *(head|grep -q|grep -m1)'` on the implementation census
  lists `:931,:969,:1051,:1426,:1501` (and `:1783`/`:2175` protected by `|| true`); count of the whole construct 26 base →
  24 impl (§F).
- **R42-C1-SCRATCH-FALLBACK-TMP.** `sed -n 298,304p tools/score-size-invariance-r42.py` and the `tempfile.gettempdir()`
  probe (§H).

## 3. Checked and clean (no row; these are deliberate, measured absences)

- Declared census sites: base `:692` (`printf \| grep -q '^error:'`), `:694` (`\| grep -m1 '^error:'`), `:1621`, `:1635`,
  `:1641`, `:1652` (`\| head -n3`/`-n1`) all match the declaration exactly — no number-drift.
- Before column of the declaration matches `before/c1-before.jsonl`: `invariant 3`, `non_invariant
  [P1,P3,P6,U1,U2,U3,U4]` ⇒ the invariant three are P2/P4/P5; P1/P3/P6 large `rc=0` (HEALTHY where BLOCKED is due);
  U1-U4 large `rc=141`; `ns_invariant 0` on N1/N3/N6; `selftest PASS (128 cases…)`; `default_equal 1`; `exit_code 1`.
- Selftest 128 → 130 cases: `check` calls 125 → 127, `R42-C1` labels 0 → 2, badges 128 → 130 (`impl/c1-able-to-fail.txt`).
- Digests: both frozen counters and both runners equal the declared sha256 (`§B`); `sha256sum -c SHA256SUMS` in
  `frozen/src` → `scrub.c: OK`, `CHANGES: OK`.
- Implementation diff: all eight hunks fall inside `probe_packages` (`:654`), `probe_update_safety` (`:1552`) and
  `run_selftest` (`:1931-3109`) — the kill rule's hunk boundary holds. Caveat for a mechanical reader: git labels the two
  selftest hunks `@@ … @@ STUB` (the fixture heredoc is the nearest recognised context), so a check that parses hunk headers
  for a function name would misclassify them.
- Registry: 236 rows at base, 239 at freeze and tip; W04 40 in both registry receipts; base receipt has its export header.
- Battery outcomes equal the declaration's expected lines: C1 `should_fail_accepted 0, control_accepted 1` (K6 PASS,
  everything else FAIL); C2 `should_fail_accepted 0, control_accepted 1` (K3 PASS as declared for forged records, rest FAIL);
  C1-K4 is cleanly attributable (`invariant 6`, `ns 3`, only U1-U4 red); K7/K8 fail only on the production-path legs.
- C2 binding: `bound()` reads only `w2-dispatch.json`/`w2-results.json`/`w2/<name>.md`; the round-41 results file has the
  same shape (`{lane,round,wave,seats,results:[{name,agent,output,…}]}`), so the binding is not structurally dead;
  `--sessions` default resolves and seat transcripts exist one level down (`…/2026-10-26T15-10-…/MistakesSweep-2.jsonl`),
  so `transcripts_bound` is a live check, not a vacuous zero.
- C2 entry rows I spot-read: SC2's field order matches `scrub_write_file` (`scrub.c:843-895`); SC4's folding matches
  `_SCRUB_FS_STAT_ZMIN/ZMAX/MIN` with `init_fs_stat` setting `finished = 1` and the status word at `:340-344`; SC5's
  `if (ret < 0) limit = 0;` is at `:1219-1220`; SC1's `_tmp` is the literal passed at `:917`
  (`scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp")`). No false cell found in the rows I read (the row-by-row review is
  the w1 C2 seats' item, not mine).
- `before/c2-before.jsonl`'s `snapshots_ok false` at the base is expected (snapshots exist only from the freeze commit), not
  a mistake.

## 4. What I did not do

- No counter (`score-size-invariance-r42.py`, `check-scrub-record-r42.py`) and no `tsukuroi-census.sh --selftest` run;
  every able-to-fail statement above is a re-score plan with today's red case named, not an executed check.
- No `jj` command: `jj` snapshots the working copy on invocation, which would touch the lane's jj state, so the
  "base = lane tip at round start" claim was taken from the commit log and the declaration, not re-derived from
  `jj-lane.sh state`.
- No edit, add, commit, checkout or stash in the lane; the only lane writes are this report and
  `.ufo/waves/round-42/w1/MistakesSweep-2/receipts.txt`.
- No package, service, mount, sysfs or boot change; no `btrfs scrub`/`btrfs device stats -z`; no `/tmp` build.
