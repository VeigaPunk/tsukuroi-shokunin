VERDICT: defect-found

Axis attribution (depth) and non-restatement hold. Two defects stand inside the claim's evidence chain:
(1) the novelty conjunct is candidate-independent and its tokens are hand-picked code identifiers, so it
can neither credit nor reject any entry; (2) the counter's "reads the rule cell" is a substring/token test —
a rule cell that says nothing (eight unordered token lists) or the opposite of the source (in non-negated
words) still scores 8/8, i.e. the exact R39-CONTENT-UNREAD class survives in shapes the frozen controls do
not cover. One host cell in the entry (EX5) is also false and not capture-derived.

Scratch: `/fast/scratch/hyaku/tsukuroi-r40/C2CritAxis/` (clone + three variant commits), removed after the
receipts were copied to `.ufo/waves/round-40/w1/C2CritAxis/`. No lane file written, no git/jj mutation in the
lane, no host mutation, no install or upgrade.

## 1. Is the entry a restatement of held knowledge? Mostly no; two host cells are

Measured by replacing all eight rule cells with the nearest sentences the base already holds
(`.ufo/waves/round-40/w1/C2CritAxis/variant-rule-cells.txt`, variant V4 `82d0a15` in the scratch clone):
TO8 and its r39 append for EX1/EX2, the SKILL child-env row for EX3, TO4 for EX4, TO3 for EX5, r38 counts for
EX6, HO4 for EX7, r35's NoUpgrade paragraph for EX8. Result:

```
$ python3 tools/check-exec-environment-r40.py --repo <clone> --branch restate --revision 82d0a15
{"result":"FAIL","rules_verified":0,...}   V4.json, row reasons:
EX1 rule lacks tokens: working directory, `/`        EX5: tmp/alpm_XXXXXX, .INSTALL, 01777
EX2: stdin, end-of-file                              EX6: stdin, sorted, duplicate
EX3: SHLVL, umask, 0022                              EX7: Depends, running, satisfy dependencies
EX4: /usr/bin/bash, /bin/sh, -c                      EX8: file list
```

So none of the eight rule cells is recoverable from the held notes; the held corpora at
`53b294a` simply do not state these mechanisms. The lane already recorded that: the round-39 Gate says the
four residual propositions is "not carried — defer" and "No TO or HO row states them"
(`corpus/lessons/round-39.md:56`), naming `hook.c:519-529`, `hook.c:258-279`, `util.c:677-683` and
`trans.c:357-358` as the re-grounding points. The entry is the planned flip of that Gate row, not a re-run.

Cell-level accounting (8 rows x rule/value/host = 24 content cells):

| cell | held at base? | evidence |
|---|---|---|
| EX2 host "TO8 carries both streams…one merged stream" | **yes, restated** | `pacman-transaction-order-r39.md:78` (base): "The child's stdout **and** stderr are both joined to the pipe whose lines become `[ALPM-SCRIPTLET]`" |
| EX6 host "14 of 69 effective hook files carry `NeedsTargets`" | **yes, restated** | `pacman-hook-order-r38.md:13-14` (base): "69 effective hooks from 70 files … 14 with `NeedsTargets`"; the override sentence is S007/S008, held at r38:5-7 |
| EX8 host ".pacnew outcome still triggers" | half derived | NoUpgrade/.pacnew outcome held at `pacman-backup-files-r35.md:30-32`; the trigger-match half is new |
| 8 rule cells, 8 value cells, EX1/EX3/EX4/EX5/EX7 host cells | no | V4 above; base has no `SHLVL`/`umask`/`scriptlet-shell` statements (base-hit receipt) |

Restated share: ~2.5 of 24 content cells (~10 %), all in the host column. That is a redundancy/authority
note (three writers for "14/69": r38 counter, r40 capture, EX6 cell), not a novelty failure.

## 2. Depth or coverage? Depth, as declared

- Base `corpus/knowledge/` 84 files -> candidate 85 (`git ls-tree --name-only <rev> corpus/knowledge/ | wc -l`).
- `corpus/SOURCES.md` 218 -> 225 rows; of S219–S225, **four re-register artifacts the base already mined**:
  S221 util.c = S216, S222 trans.c = S210, S223 hook.c = S208, S224 alpm-hooks.5 = S209 (base rows, same
  commit `54d9411`). Only S219 meson_options.txt, S220 PKGBUILD and S225 own-work capture are new artifacts.
  That is legitimate registry work (the Gate asked for new rows because the held rows' anchor/scope cells do
  not cover these lines), but "new mined upstream rows" is bookkeeping, not new source ground.
- No new surface: C2 touches the entry and SOURCES only (`SCORECARD.md:2319-2320`); PROVINCE's planes and the
  census are untouched. Therefore depth, not coverage — the declaration's axis row is right.

The depth is real where I spot-checked the source (not only tokenized): EX1–EX3 hold at
`.ufo/waves/round-40/frozen/src/util.c:655-705` (`chdir(handle->root)` :628, `dup2(child2parent_pipefd[HEAD],1/2)`
:664-665, `dup2(parent2child_pipefd[TAIL],0)` :666, `setenv("SHLVL","1",0)` :692, `unsetenv("BASH_ENV")` :694,
`umask(0022)` :695); EX6 holds at `hook.c:519-526` (`alpm_list_msort(…strcmp)`, `_alpm_strlist_dedup`,
`buf[len++]='\n'`); EX7 holds at `hook.c:508-517` and `:645-668` (`running '%s'...` written before
`_alpm_run_hook`, `ret=-1` only when `hook->abort_on_fail`, Pre-phase `break`). EX4's host index 1277 checks
out live (`strings /usr/lib/libalpm.so.16.0.1 | grep -n -x /usr/bin/bash` -> `1277:/usr/bin/bash`).

## 3. Would a do-nothing control reach the target? No — but one conjunct is free

`controls/controls.jsonl` K0 (`53b294a`, do-nothing): `exit 1, rules_verified 0, source_ok 0, counts_ok 0,
novelty_base_hits 0, FAIL`. The target is not reachable by doing nothing. But the novelty conjunct is
satisfied by doing nothing, and (see §4) by every candidate — it is the one predicate term with no
discriminating power.

## 4. Are the novelty tokens a fair premise or chosen to be absent? True as a premise, non-evidential as a test

All eight tokens are 0 at base — verified independently with the counter's own command (`git grep -F -c` at
`53b294a` over `corpus SKILL.md PROVINCE.md`; `.ufo/waves/round-40/w1/C2CritAxis/base-novelty-hits.txt`):
`chdir("/") 0, socketpair 0, SHLVL 0, scriptlet-shell 0, alpm_XXXXXX 0, _alpm_strlist_dedup 0,
could not satisfy dependencies 0, match_noextract 0`. The premise is literally true and was frozen before the
seats. Three reasons it is not a fair *test* of novelty:

1. **Candidate-independent.** `novelty_hits` greps the constant `BASE`
   (`tools/check-exec-environment-r40.py:212-219`, used at :327-329), never `b.sha`. No candidate entry can
   change the value. Proof from the candidate receipt itself: `.ufo/waves/round-40/after/c2-after-bf23805.jsonl`
   reports `novelty_base_hits 0` for an entry that contains six of the eight tokens
   (`grep -c -F` in the entry: `chdir("/") 1, SHLVL 2, alpm_XXXXXX 1, satisfy dependencies 1,
   match_noextract 1, scriptlet-shell 1`). A conjunct that is constant across the space of candidates cannot
   discriminate PASS from FAIL; only a base-corpus mutation could, and that is not a candidate.
2. **Chosen to be absent.** Five of eight tokens are upstream C/meson identifiers (`chdir("/")`,
   `socketpair`, `alpm_XXXXXX`, `_alpm_strlist_dedup`, `match_noextract`), two are environment/packaging
   strings (`SHLVL`, `scriptlet-shell`), one an error message. A prose corpus that cites code — which this
   one is — cannot contain those unless it quotes them. The base does contain the prose synonyms and the
   *held* words: `_alpm_run_chroot` 4, `ALPM-SCRIPTLET` 43, `NoExtract` 40, `NoUpgrade` 50, `.pacnew` 50,
   `NeedsTargets` 6, `Depends` 9, `AbortOnFail` 9, `BASH_ENV` 16 — all excluded from `NOVELTY`
   (`tools/check-exec-environment-r40.py:95-96`), while `umask`, which is also 0 at base, is not listed
   either. The set is a hand-picked subset of zero-hit strings, not a test of the knowledge.
3. **The frozen-zero pattern is now two rounds old.** Round 39's C2 predicate carried the same shape
   (`oracle_violations == 0`, `tools/check-transaction-order-r39.py:33`, scored "oracle 0" in
   `SCORECARD.md:2250`). A frozen capture/base statistic can falsify a host-consequence sentence but cannot
   credit an entry; carrying it inside the PASS predicate is calibration debt, not evidence.

Smallest safe correction: drop `novelty_base_hits == 0` from the predicate (report it as a frozen premise in
the receipt) or replace it with a per-candidate overlap test — the entry's rule/source cells must carry tokens
that the held entries (`pacman-hook-order-r38.md`, `pacman-transaction-order-r39.md`,
`pacman-backup-files-r35.md`) do not — which is measurable at `b.sha`.

## 5. The counter's rule read is substring-only; R39-CONTENT-UNREAD survives in unfrozen shapes

Two variants, each a single-file change to the entry in the scratch clone, committed with the fixture identity
and run with the frozen counter (`sha256 d4a2bb94…`, verified equal at `a447b67` and at the tip):

**(a) V2 `ca43edd` — the opposite of the source, in affirmative words.** EX3 rule replaced by: "Before
`execv` the child keeps every inherited `SHLVL` value unchanged and leaves `BASH_ENV` set in the environment,
and it drops every other variable of the calling pacman process, while umask 0022 is applied after execv
returns to the parent" (contradicts util.c:692-695 and the row's own value cell `BASH_ENV=unset`).
Result: `PASS, rules_verified 8` (`w1/C2CritAxis/V2.json`). The polarity test is a word list
(`NEG`, counter:97) — "keeps", "leaves … set", "drops" are not in it, and nothing compares the rule text with
the `value` cell it sits beside.

**(b) V3 `83227b7` — rule cells that state nothing.** All eight rule cells replaced by unordered token lists,
e.g. EX3 = "SHLVL BASH_ENV umask 0022 execv child environment variable inherited signal handlers set remove",
EX8 = "Path trigger file list names package NoExtract skipped matching ignores NoUpgrade .pacnew protected file
listed name installation root". Result: `PASS, rules_verified 8`, every row `reasons: []`
(`w1/C2CritAxis/V3.json`). That is precisely the routed defect's wording — "an entry whose rule cells said
nothing … scored 8/8" (`corpus/lessons/round-39-verifier-spotcheck.md:§6.1`) — still reproducible. The round-40
amendment closes the two frozen shapes (K1 `RULE NOT SUPPLIED`, K2a negation-worded falsehood) and the
quote-copied shape (K5), not the class. The docstring's promise "every rule row is credited only when its RULE
cell itself carries the rule" (counter:14-27) is therefore true only for the literal controls; the `value` cell
is source-derived (counter:145-181) and cannot be gamed, the `rule` cell can.

Smallest safe correction: add a per-row frozen **affirmative sentence pattern** derived from the source the
way `VALUES` is (counter:145-181), require at least one match per row, and fail on the matching contradiction
patterns. Examples that would have killed both variants while passing the candidate: EX3
`sets?\s+`?SHLVL``, `(removes?|unset)`?BASH_ENV``, `umask\s*\(?0022`; EX1 `working directory\s+`?/``; EX6
`NeedsTargets` within the same sentence as `stdin` and (`sorted`|`one .*per line`); EX8 `file list` within the
same sentence as `Path` and `matches?`.

## 6. One host cell is false, and the front-matter provenance claim is too strong

EX5's host cell (`corpus/knowledge/pacman-exec-environment-r40.md:25`) ends "on this host `/tmp` is a tmpfs".
Measured read-only today (`.ufo/waves/round-40/w1/C2CritAxis/host-checks.txt`):

```
$ pacman-conf RootDir                                   -> /
$ findmnt -no TARGET,SOURCE,FSTYPE /tmp                 -> /tmp /dev/nvme1n1p1 xfs
```

Root is `/`, so `<root>/tmp` is that xfs mount, not tmpfs; the lane already says so at `PROVINCE.md:176`
("the second NVMe device (`/tmp`, `/fast`) is unread"). The frozen capture cannot produce the claim either:
`.ufo/waves/round-40/frozen/hostcap/MANIFEST.sha256` lists three files (capture-meta, hooks-needstargets,
libalpm-shell-strings), none of them a mount record. The entry's front matter says "the host column comes from
a frozen read-only capture" (`:13`); in fact only EX6's count and EX4's presence clause are capture-checked
(`counts_ok`, counter:321-326), while EX4's "lacks `/bin/sh`", EX5's tmpfs clause and EX7's "0 such errors"
are live claims. I verified the two true ones live (`strings … | grep -x /bin/sh | wc -l` -> 0;
`grep -c 'could not satisfy dependencies' /var/log/pacman.log` -> 0); EX5's is false. No rule or value cell is
affected — the source-level EX5 rule stands — but a reader who trusts the host column takes a wrong fact about
this host, and the counter cannot see it.

Smallest safe correction: replace the clause with the measured mount (`/tmp` is xfs on `/dev/nvme1n1p1`, so a
scriptlet's `tmp/alpm_XXXXXX` is created there), cite `findmnt -no TARGET,SOURCE,FSTYPE <root>/tmp`, and
narrow `:13` to "the host cells are read-only captures or the command printed in the cell".

## 7. Impacted axes

| axis | impact |
|---|---|
| depth | **holds** as the axis of the move (§2) and the rules are source-true where spot-checked; the host-cell error (§6) and the gameable rule read (§5) weaken the evidence, not the entry's rules |
| coverage | unchanged — no new surface; four of seven SOURCES rows re-register held artifacts |
| freshness | the host column is a mix of held restatements (EX2, EX6), live reads (EX4 absence, EX7) and one false claim (EX5); a future pacman/capture change leaves three authorities for "14/69" |
| calibration | the candidate-independent frozen-zero conjunct is carried a second round (§4.3); the counter's promise about reading the rule cell overstates what it tests (§5) |

## 8. What I did not do

I did not re-derive EX4/EX5's source rules from `trans.c`/`PKGBUILD` line by line, did not judge the
round-40 C1 claim, did not run any sibling lane's tool, and did not run the census. The variant revisions
exist only in the removed scratch clone; their diffs and entry digests are kept in
`w1/C2CritAxis/variant-rule-cells.txt` and `w1/C2CritAxis/counters-receipt.json`.

Receipts: `w1/C2CritAxis/{candidate,V2,V3,V4}.json`, `counters-receipt.json`, `base-novelty-hits.txt`,
`host-checks.txt`, `variant-rule-cells.txt`.
