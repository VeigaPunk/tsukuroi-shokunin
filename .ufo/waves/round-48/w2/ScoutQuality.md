VERDICT: defect-found

# ScoutQuality — Item F-2: QUALITY.md sweep at ae99f021b76f8eb1c8805d32d80644464afb1ff6 (FREEZE)

Method: `git show ae99f021…:corpus/QUALITY.md` (183 lines, 93 numbered criteria, read whole — scratch copy `QUALITY.md`), the three frozen counters read whole, the census diff BASE→FREEZE, the frozen declaration (`SCORECARD.md:3090-3115`), FROZEN.md, the three committed battery drivers + summaries, `make-w2-spec.py` read whole, the adjacency diff, and two read-only runs of my own (below). `w1/` was never opened (void by rule).

Checks I ran myself (copies in `ScoutQuality/` receipts):
- `python3 tools/check-registry-coverage.py --revision ae99f021…` → `status FAIL, findings 3 REGISTRY-ROW-MISSING: tools/check-scrub-admission-r47.py, tools/check-scrub-admission-r48.py, tools/score-selftest-tmpdir-r48.py` (receipt `ScoutQuality/registry-coverage.out`).
- `python3 tools/check-scrub-admission-r48.py --revision ae99f021…` → `{structural_ok 1, quotes_ok 3, verdicts_ok 0, marks_ok 0, base_ok 1, waves_seen ['w2'], verdict FAIL}`; all seats `dispatched 0 times` (fails closed, does not crash on absent `w2-dispatch.json`/`w2-results.json`); the committed `w1-dispatch.json` was not read (`waves_seen` is exactly `['w2']`).
- `sha256sum` of `git show ae99f021…:tools/tsukuroi-census.sh` = `375aa737…e2426` = `frozen/census.sha256` = FROZEN.md:9. My own recomputation of the three GR section extents reproduces `frozen/gr-section-hashes.json` byte-for-byte (GR1 `fe77ac76…`, GR2 `e0b391e1…`, GR3 `43430a14…`).
- Did NOT re-run the C1 counter (~5–10 min, six selftests): the committed K-pass control already exercised it (battery-c1.jsonl:5). Did NOT re-run `check-self-assessment.py` (it runs a selftest internally); the committed battery records its outputs at base and impl (battery-c3.jsonl:1-2).

Statuses: PASS / FAIL / DEFERRED (touching round-end or wave obligations that freeze bytes cannot settle — with the freeze-state noted) / N/A.

## Per-criterion sweep (1–93)

| # | Status | Evidence |
|---|---|---|
| 1 falsifiable | PASS | Every claim carries a frozen predicate string and kill rule: `SCORECARD.md:3104-3106`; predicates repeated verbatim in counter code (`score-selftest-tmpdir-r48.py:56-57`, `check-scrub-admission-r48.py:81`) and FROZEN.md:20-22. |
| 2 measured anchor | PASS | `before/…` + `controls/battery-summary-*.jsonl` cite concrete legs; FROZEN.md:9-13 pins every artifact by sha256. |
| 3 obs/inf/unk separate | PASS | Fixture vs live separated and labeled (`battery-c2.jsonl:14` "fixture, not the live integration"; `battery-c3.jsonl:5` "synthetic; the live final is the claim"). |
| 4 errata append-only | DEFERRED | Record-file edits bind at integration; note the freeze itself carries an in-place edit (`adjacency-anchors-r19.json` IN-109 found_line 2593→2642) that criterion 60 will have to disclose. |
| 5 rejection kept | PASS | `SCORECARD.md:3095-3096`: void w1 "are incident evidence only and are never scored" — retained, not dropped. |
| 6 pacman advice cites S010 | N/A | No pacman advice anywhere this round (spec line 48 re-issues the standing pause). |
| 7 SOURCES row/tier | DEFERRED | Declaration flags sourcing pending ("opened this round", `SCORECARD.md:3104-3105`); SRC-N1..N3 seat items carry the registry-bar instructions (`make-w2-spec.py:198-202`). |
| 8 unknown sweep + entry headers | N/A | No new `[unknown]`; GR rows are existing knowledge re-verified. |
| 9 negative claim bounded | PASS | "never /tmp" is bounded: wrapper-logged `mktemp` resolutions (`score-selftest-tmpdir-r48.py:17-18,95-99`), failfast legs assert zero creations (:106-112), plus `TExecStrace` item C1-X6 audits writes by syscall trace (`make-w2-spec.py:101`). |
| 10 correction sweep | DEFERRED | No correction commit yet; SKILL/README mark edits are the L1's integration step. |
| 11 LOG entry with evidence | DEFERRED | `ScribeLog` item F-5 drafts it (`make-w2-spec.py:213-214`); commit lands at round end. |
| 12 absent tool → source first | PASS | proc_pid_fd(5) + Bash manual opened LIVE by `SScoutProcFd`/`SScoutBashRedir` (`make-w2-spec.py:197-200`) instead of tag-[inference]. |
| 13 EACCES triage | N/A | No permission-denial finding this round. |
| 14 QUALITY check for new entries | N/A-light | No new entry; the existing entry carries `## QUALITY check` (scrub-entry.md:238). |
| 15 root metadata findings | N/A | No metadata findings. |
| 16 metadata policy sources | N/A | No metadata-health grading. |
| 17 unit-permission scoping | N/A-light | GR3 cites `systemd.kill.xml`/btrfs-scrub@.service (mechanism lines, not permission-policy overreach); no "only/not-configured" claim about ProtectSystem. |
| 18 fixture-vs-live + bot attribution | PASS | Fixture/live labels consistent (see #3); no bot claims. |
| 19 claim/source scope | PASS | Every `**Quote.**` line names `S###` file:line + quoted text verified as substring of the digest-pinned snapshot (`check-scrub-admission-r48.py:79,252-267`; observed `quotes_ok 3` at FREEZE). |
| 20 comment attribution | N/A | No bot/comment claims. |
| 21 portable locators | PASS | Rows bind by sha256 section extents (:145-159); snapshots pinned by digest (`:45-68`); no bare line-range citation anywhere in the counters. |
| 22 positive domain | PASS | Counter predicates assert positive observed facts only; the absent-w2 state is reported per seat (`dispatched 0 times`), not globalized. |
| 23 section/table citation resolution | PASS | `section_hashes` binds exact `## GR<n>` extents and fails closed on duplicated/missing/inner headers (:126-142; battery F1a FAIL, c2.jsonl:13); QUOTE_RE verifies row text on pinned bytes. |
| 24 execution/evidence scope | DEFERRED | Wave runs post-freeze. Freeze-state risk: see #31. |
| 25 image-typed verdicts | N/A | No boot-image verdicts. |
| 26 L1 scope | N/A | No steer narrower than the standing pause; no L1 probes run yet. |
| 27 gate revisions landed+hex | N/A (scope) | These are **measurement** counters, not binding gates — they must accept unlanded sandbox revisions (battery-c2.py scores sandbox `HEAD`s). C2 adds a `merge-base BASE` check (:315-317); C1/C3 `^{commit}`-resolve only (`score-…:187`; `check-self-assessment.py:128`). The binding-gate tools this round (`check-registry-coverage.py`, `check-seat-scope.py`) do import `_revision`. |
| 28 `_revision.py` import | N/A (scope) | Same carve-out: "keep the measuring judge independent of that module" (QUALITY.md:38). The r48 counters are the judges; the r30+ pattern keeps counters independent. Note: `check-self-assessment.py` also bypasses `_revision` (line 128 own `rev-parse`), an older inconsistency this round inherits. |
| 29 final-evidence tail | DEFERRED | Round-end report obligation. |
| 30 whole-proposition locators | PASS | IN-109 repin preserved the verbatim `evidence_quote` and appended the move inside `note` (diff `adjacency-anchors-r19.json:2465-2473`); counters cite verbatim predicates (`predicate` key in every output line). |
| 31 seat execution class | DEFERRED — risk flagged | `make-w2-spec.py` `add()` emits `name/role/axes/milestone/prompt` only; no `EXEC-AUTHORIZED` marker in any prompt and no `Scope: executed=` trailer instruction (verified by reading the whole generator; CONTEXT:52 specifies only `VERDICT:` first line). `tools/check-seat-scope.py:41,77` flags `SCOPE-UNDECLARED` (missing trailer) and `SCOPE-EXEC-UNAUTHORIZED` (declared commands without the marker): if that gate runs on w2, every executor seat reads red as generated. Routed observation for the L1, not settled at freeze. |
| 32 sibling anchors quote+blob | PASS-lite | The IN-109 inbound row keeps `evidence_quote` verbatim and records `found_line 2642` with a DRIFTED class and dated move note — exactly the inbound-pointer contract (`adjacency-anchors-r19.json` diff; truncated tail of `note` not shown here was read via `git show`). |
| 33 /boot writer attribution | N/A | No boot-plane audit. |
| 34 operative contract | PASS | Counters encode the operative predicate verbatim and print it (`predicate` field); no registry-row selection prose is claimed. |
| 35 declaration attribution | N/A | No sibling "Owns" claims. |
| 36 object identity before refs | PASS | Counters digest-pin blobs (`SNAPSHOTS`, section extents, `census_sha256`); `rev-parse^{commit}` resolves object identity before use. |
| 37 busybox applet dispatch | N/A | No exec-log classifier touched. |
| 38 reviews bind candidate bytes | PASS | Bind requires `SECTION SHA256: <hex>` equal to the current row hash for credit (`check-…:334,341`) and prints `census_sha256`/`section_sha256` in output (`score-…:203,229`; `check-…:349`). |
| 39 refusal echo vs status | N/A | No `CANNOT_EVALUATE` channel in these counters; errors print `verdict FAIL` with `error`, never echo a selector as accepted (`score-…:190,198`; `check-…:305`). |
| 40 binder type controls | N/A | No tag/blob binder. |
| 41 oracle independence | PASS | Expected values are code constants/hashes (SUMMARY_PASS :55, CASES :45, frozen digests), never derived by running the artifact under test. |
| 42 reviewed bytes persisted | PASS | `frozen/gr-section-hashes.json`, `frozen/census.sha256`, FROZEN.md committed before any seat; battery receipts committed pre-dispatch (ls-tree shows all under the freeze commit). |
| 43 consumer type coverage | N/A | No type matrices this round. |
| 44 dead/malformed evidence visible | PASS | `bind()` returns per-seat typed reasons (`dispatched 0 times`, `report too short`, `not exactly one results entry`, :180-206); the void w1 is retained and disclosed, not deleted. |
| 45 column-bound type propositions | N/A | No decision-gate table parser. |
| 46 declarations audited | DEFERRED | Same family as #31: reports not written; generated prompts lack the trailer this gate wants. |
| 47 prompt scope ≠ prevention | DEFERRED — risk flagged | `check-seat-bindings.py` audits frozen per-seat literal scopes; w2 items embed commands in prose prompts and carry no structured read/write path lists, so this audit will have less to bind. Same routed observation as #31. |
| 48 cohort accounting | DEFERRED | Seat reconciliation is a post-wave duty; the counter already reports every universe seat individually (:331-333). |
| 49 quality trend evidence | DEFERRED | Any `quality:` change must name a superseded entry at round end. |
| 50 structured edit authority | N/A | No structured-edit claims. |
| 51 reconcile units/identities | N/A | No count reconciliation claimed. |
| 52 finite carriers + linkage | PASS | Entry's extent defined by exact `## ` headings only; fence/comment cannot extend a row (:139-141 rejects inner `## `). |
| 53 normalization discriminates | PASS | `norm()` collapse applies only to the quote-vs-line comparison (:250,264); seat/citation classes stay distinct (blocking vs unbound vs credited, :336-341). |
| 54 summary names recoverable | PASS | Battery rows echo the counter's own keys (`legs`, `census_sha256`); c1.jsonl:5 digest `375aa737…` = FROZEN.md:9. |
| 55 premise capture time | PASS | `c1-live-r48.txt` header `2026-10-28T11:19:26Z`; BASE/FREEZE named in every artifact. |
| 56 redaction one-class | N/A | No redaction labels. |
| 57 self-assessment re-measured | PASS | C3 measures at the named revision against repo bytes; base→impl drift honestly declared (`SCORECARD.md:3106`: 1 at base, 3 at impl until restated; battery-c3.jsonl:1-2 observed). |
| 58 sudo allow-list | N/A | No privileged commands in any item (grep of make-w2-spec.py: `sudo` absent; context line 48 re-issues the pacman pause). |
| 59 scratch clone no push path | **FAIL** | `battery-c2.py:45` and `battery-c3.py:38` run `git clone -q --shared <LANE>` — the clone inherits `origin=<LANE>` with a live push path and neither file disables `pushurl`/`remote.origin.pushurl` (grep: `pushurl` absent from both). The spec instructs seats to clone the same way (`make-w2-spec.py:47`). No push *occurred* (fixture commits use `-c user.name=ctl` inside the sandbox only), so this is a contract violation by letter, not a demonstrated push. |
| 60 non-append sweep disclosed | DEFERRED — owed | Round-48 lesson must disclose: `adjacency-anchors-r19.json` two in-place changed lines (IN-109), any SCORECARD non-append lines, and every post-freeze record-file edit (GR marks, SKILL/README marks, restated axes table). |
| 61 source-row Gate record | DEFERRED — owed | Sourced C1/C2 plan to open S-rows this round (SCORECARD.md:3104-3105); each new row needs its `## Gate` record in `corpus/lessons/round-48.md`. |
| 62 ordinals from measured outcomes | PASS | Declaration ordinals (depth 8, coverage 9, …) come from the round-44/45 measured surfaces; C3's ordinal checks read those sections, not declaration prose. |
| 63 mechanism wording pre-source | PASS-lite | The declared mechanism describes our own committed bytes (`selftest_base_dir`, `eval "exec ${fdn}<\"$base\""`, traps — census diff @2049-2111), not an upstream premise; the source-side is flagged pending ("opened this round"), matching the criterion's marking intent. |
| 64 table-cell shapes | N/A | Counters read headings/regexes, not a Markdown cell parser with quoted-shape variants. |
| 65 ordinal not self-read | PASS | The C3 counter reads the latest axes/`measured outcome` heading (round 44/45), never the round-48 declaration (`check-self-assessment.py` heading selection; K10/K13/K17 read the older table — mismatches are content, not self-reference). |
| 66 teaches keeps branches | N/A | No new teaches text; GR2's corrected attribution is the amended content the counted seats judge. |
| 67 companion sweep | DEFERRED-lite | IN-109's register edit updated the JSON row's own fields (quote, found_line, note) in one commit; whether a normative md/`SKILL.md` companion also carries that line is for the L1's landing commit to confirm (no companion field found in the row). |
| 68 frontier sweep | PASS | Declaration claims "deeper ground"/re-admission, not new-frontier coverage; the only frontier surface is delegated to seat `ScoutConsider` item F-1. |
| 69 sibling pointer replay | PASS-lite | Inbound register row replays the quote on the moved line (its `evidence_quote` is byte-stable while `found_line` drifted — the criterion's DRIFTED path executed correctly and was recorded). |
| 70 tool lands with registry row | **FAIL** | `check-registry-coverage.py --revision ae99f021…` → `findings 3 REGISTRY-ROW-MISSING`: `tools/check-scrub-admission-r47.py` (inherited r47 debt), `tools/check-scrub-admission-r48.py`, `tools/score-selftest-tmpdir-r48.py` (this round's new counters). Gate is red at FREEZE; the same-round clause is still satisfiable at integration (SKILL.md registry rows). |
| 71 companions agree verdicts | DEFERRED | The three admission marks (entry/SKILL/README) are the multi-file verdict companions; they land at integration on a counter PASS (`GScribeMarks` drafts them, `make-w2-spec.py:159-160`). |
| 72 should-fail before proof | PASS | 13 FAIL-showing C2 controls + 4 FAIL C1 controls + 4 FAIL C3 controls all `as_expected true` before any seat (battery summaries). |
| 73 battery = counting command | **FAIL (letter)** | The declaration's counting commands are the bare counters (`SCORECARD.md:3104-3106`), not the battery; declared measure is the counter predicate, not a `should_fail_accepted` field. Batteries are committed pre-data controls (intent honored); the letter of 73 is unmet — flag for L1 restate-or-deviate. |
| 74 GIT_* strip (git writes) | **FAIL (scope: drivers)** | Counters spawn only git *reads* (out of this criterion's tool-scope), but `battery-c2.py`/`battery-c3.py` run `git add`/`commit` in sandboxes with the ambient env (`subprocess.run` without `env`, :23-25,94-95 of each); `GIT_DIR`/`GIT_INDEX_FILE` inherited from a caller's environment could leak into those commits. |
| 75 attribution by trace/disclosure | N/A | No seat cancelled/blamed this round. |
| 76 owed statements frozen | DEFERRED | Owed items from prior routed defects, if carried, need the marker pattern in the round-48 lesson. |
| 77 revision-cited receipt | **FAIL (letter)** | Declared before-values cite `battery-summary-r48-*.jsonl` K0 rows (`SCORECARD.md:3100-3103`) — plain JSON rows with case/legs/verdict, NOT `tools/run-receipt.py` headers (`revision`, `tool`, `tool_sha256`, stdout reproduction, `exit_code` footer). Partial mitigation: `census_sha256` digests inside the rows bind the measured blob; tool bytes are not digest-bound. |
| 78 git child env contract | **FAIL** | The two new counters spawn git children with the ambient environment: `score-…:187` (`subprocess.run(['git','-C',…])`, no env), `check-…:103-104` (`git()` helper, no env) — no `GIT_*` drop, no `GIT_CONFIG_GLOBAL/SYSTEM=devnull`, no private `HOME`. Contrast `check-self-assessment.py:69-107` and `check-registry-coverage.py` (`CHILD_ENV_BASE` + clean_env) which implement the contract. Battery drivers likewise inherit ambient. The r30+ child-env contract exists in `tools/_revision.py` (`clean_env`) and was not reused. |
| 79 depth row digest+marker | PASS (adapted) | C2 binds rows by sha256 extents + required Quote lines on digest-pinned snapshots; markers leg `marks_ok` requires the exact heading lines in entry/SKILL/README (:360-363). |
| 80 falsifiable + controls | PASS | Frozen predicate identical in declaration/counter/FROZEN; all snapshot digests pinned; cheapest controls committed pre-data: do-nothing (K0), marks-only (K1), forged cohort (K2), forgery variants (K3*, K6-K8, F1a), synthetic PASS (K9). Novelty-token clause N/A (admission, not novelty). |
| 81 scripted nonreader below target | **FAIL (letter)** | Battery K9 is a scripted fetch-and-fill writer — synthetic reports with template bodies (`battery-c2.py:77-78,85-89`) that satisfy every mechanical predicate and score PASS (c2.jsonl:14). The criterion requires that writer to read BELOW target; here it reaches it. This is a deliberately disclosed limit (`GSentForge` item C2-S1 names it "the standing documented limit", `make-w2-spec.py:149-150`), not a hidden hole — but by criterion 81's letter it is FAIL. |
| 82 fixture-gated + live views | PASS | `controls/c1-live-r48.txt` (env-scrubbed live run, header `read-only`, capture time 11:19:26Z) and `c1-live-r48-normalenv.txt` are the two committed live views; `c2-selftest-scratch-after.txt`/`c2-selftest-spaced-after.txt` are full selftest outputs in both TMPDIR classes; `TExecLiveKill` X7 independently re-verifies live bytes unchanged (`make-w2-spec.py:102-103`). |
| 83 verdict per-conjunct grounds | DEFERRED | Applies when a claim files not-verified or a closure changes it — post-measurement only. |
| 84 echo only validated tokens | N/A | No new machine-grammar line emitted by the fix (selftest summary format unchanged). |
| 85 namespace view | N/A | Counter claims ambient-*insensitivity* (`env -i`), not a namespace indistinguishability claim; `env_for` builds a fresh dict (`score-…:68-72`) so no ambient channel reaches the census beyond the declared PATH/TMPDIR/MKTEMP_LOG. |
| 86 upstream-source rule rows | PASS-lite | GR rows' Quote lines resolve to pinned upstream snapshots (`scrub.c`, `dev-replace.c`, `systemd.kill.xml`, …); GR3's host-observation half cites `capture.txt` (S249 own-capture) alongside upstream rows — own-work + upstream mixed as the criterion allows (upstream rows present). |
| 87 content read | PASS | Counter reads verdict first lines, contradicting verdicts (:207-210), quote content (:264), citation content (:272-284) — not just structure. |
| 88 claim parameters + one-violation control | PASS | Battery arms each violate exactly one named parameter (K1 marks-only → verdicts; K2 hash; K5 role mix; K8 readme mark; F1a structure). |
| 89 guard-mechanism evasion | PASS | A2's own anti-laundering family is directly exercised: bad-citation `partly` (K3), clean-citation `partly` (K3b), self-contradiction (K3c), thin `fails` (K3d) all FAIL as required. |
| 90 observed-channel coverage | **FAIL (gap, disclosed shape)** | The counter's oracle is `MKTEMP_LOG` — an observable channel the scored code can read: a census mutant whose fixture creation unsets `MKTEMP_LOG` or invokes the real `/usr/bin/mktemp` directly produces an empty log → `loc_ok 0` (catches it) but a smarter mutant writing the fixture under `/tmp` whenever `MKTEMP_LOG` is absent from *its own* detection set (e.g. checking `argv[0]` or PATH order differently) is unarmored. No battery arm mutates the channel itself; `TCritClaim` X4's decoy-mktemp attack covers part of this family post-freeze (`make-w2-spec.py:125-126`). Graded FAIL by the per-channel letter; note also `any_fails` (:342) over-blocks a stale-hash `fails` — harmless direction (stricter). |
| 91 adopted text re-checked | PASS (by construction) | Non-counted seats produce report text only; the L1 "lands it ONLY on a counter PASS" (`make-w2-spec.py:160`, GScribeMarks item). |
| 92 one header row | PASS | New tables in FROZEN.md:7-13 and the declaration table each carry one header row. |
| 93 counted verdict binding channel | PASS | Declaration states the channel before data: seats "bind through their own report files (first two lines)" (`SCORECARD.md:3105`; counter docstring :21-23); lost records get typed `UNBOUND` details, not silent zeros (bind :180-212); counter names its one counted wave `w2` (`WAVE` const :42, `dispatches()` :162-164 ignores w1). The r45 yield-shape clause is moot for file binding; battery K7/K3c cover the analogous file-shape arms (no-dispatch, self-contradicting). |

## Freeze-state findings (not in the table above)

- F1. `w2-spec.json`/`w2-dispatch.json` do **not** exist inside the freeze commit (`git ls-tree ae99f021… .ufo/waves/round-48/` shows `make-w2-spec.py` but no `w2-*`); FROZEN.md:29's "(output `w2-spec.json`, validated, `w2-dispatch.json`)" describes the post-freeze generation step, which is consistent with the freeze-first design but worth a word of precision in the lesson.
- F2. The C2 counter at FREEZE already reads `waves_seen ['w2']` while no w2 artifacts exist — it handles absence cleanly (`dispatched 0 times`), i.e. fails closed rather than crashing; verified by my run.
- F3. A2 nuance worth recording: `blocking` (current-hash `partly`/`fails`) and `any_fails` (**any**-hash `fails`) both negate `row_ok` (`check-…:341-346`). A `fails` verdict on a *stale* hash therefore still blocks — stricter than the declared "on the current row hash" sentence; the divergence is in the safe direction.

## Three proposed criteria (exact text)

**Proposal A (TMPDIR/`--work` contract under spaced paths).**

> `94. **A counter whose claim is a scratch/TMPDIR contract exercises its own scratch contract under a spaced path (R48-COUNTER-SPACED-WORK):** when a claim's counter asserts behavior under a TMPDIR or scratch directory containing characters its subject refuses (whitespace, separators), the frozen pre-data controls include one control run whose counter invocation itself uses a spaced `--work`/scratch root and a hostile ambient TMPDIR, and that run must PASS — a counter that was only ever run under space-free scratch has not shown its own paths are safe. Falsified by: any battery row where the counter's own scratch is always space-free, or the spaced-work control leg failing while the spaced-subject legs pass. Evidence: tools/score-selftest-tmpdir-r48.py:27-29 (--work contract), controls/battery-c1.py:50 (mkdtemp always space-free), corpus/lessons/round-48.md R47-C2-TMPDIR-FALLBACK (the spaced-TMPDIR defect class this claim repairs).`

Justification: the census defect being fixed existed *because* r47 tested dirty TMPDIR only by falling back to `/tmp`; the r48 counter itself defaults `--work` to `$HYAKU_SCRATCH/tsukuroi-r48/counter-c1` and every committed battery run uses space-free scratch. The only spaced-ambient exposure is a post-freeze wave item (`TExecCounterB`, make-w2-spec.py:92-93) — exactly the gap the criterion would close at the battery level.

**Proposal B (bound negative verdicts block regardless of citations).**

> `95. **A negative verdict bound to the artifact's current bytes blocks admission independent of the report's citations (R48-BOUND-NEGATIVE):** when a counted verdict carries the scored artifact's identity (section/row digest), a `partly` or `fails` bound to the CURRENT bytes blocks admission whatever the rest of the report contains: citation defects may only remove a seat's credit, never negate its negative; a self-contradicting report is read as a negative on its own hash; and a format-thin negative still blocks. Falsified by: battery K3 (bad-citation `partly`), K3b (clean-citation `partly`), K3c (self-contradicting report), K3d (two-byte `fails`) — each must score FAIL. Evidence: tools/check-scrub-admission-r48.py:11-14,207-210,340-341; controls/battery-summary-r48-c2.jsonl:4-7; the r48 counter first-draft defect recorded for the lesson (format-thin negative vanished — caught only by pre-data battery case K3).`

**Proposal C (wave dispatch only from a committed freeze).**

> `96. **A counted wave is dispatched only against a committed freeze (R48-FREEZE-BEFORE-WAVE):** before any seat of a counted wave is dispatched, one commit holds the declaration, every counter file the counters read, every pre-data control receipt, the frozen digests of the bytes under test, and a freeze record naming that commit as `FREEZE`; the wave generator takes the freeze sha as input and names the lane tip at round start in its context; a wave spec or dispatch record produced before the freeze commit — wrong base, absent counter file, empty frozen corpus — is incident evidence, not a scored wave, and is retained and disclosed, never deleted or re-scored. Falsified by: round-48 attempt 1 — `w1` dispatched with context base `76819197` vs lane tip `5fdf062f`, no counter file, empty `frozen/src`, voided by the orchestrator (SCORECARD.md "Round 48 — declaration" incident disclosure; .ufo/waves/round-48/frozen/FROZEN.md).`

## Notes for the L1

- Routed defects (frozen-counter amendments for next round): #78 (git child env) and #73/77 (battery/receipt letter) on the two new counters; #90 channel-arm gap; #81 (K9 scripted writer reaches target — already the disclosed GSentForge limit); #59 clone-with-push-path in both battery drivers (and the spec's own fixture instruction, which inherits the same shape).
- Conformance risk to check before reports land: `check-seat-scope.py` expectations (`EXEC-AUTHORIZED` marker, `Scope: executed=` trailer) are not emitted by the w2 spec generator; if the gate is meant to run on w2, the L1 should either require trailers at integration or accept-and-disclose.
- Criterion 60 sweep is owed: `adjacency-anchors-r19.json` IN-109 (2 changed lines) plus all post-freeze record edits.
- My scratch `/fast/scratch/hyaku/tsukuroi-r48/ScoutQuality/` is removed on completion of this report write-up (receipts copied to `ScoutQuality/` first).
