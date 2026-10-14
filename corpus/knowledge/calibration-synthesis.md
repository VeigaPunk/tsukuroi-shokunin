# Calibration synthesis — what the lane measured vs what it believed (rounds 1–9)

source: read-only re-hash and re-run of landed artifacts on host `plazir27`, user `vgpnk`
(non-root, no `sudo`): `md5sum`/`sha256sum`/`wc`, `git status`/`git log`, this lane's own
`bash tools/tsukuroi-census.sh --selftest` (hermetic; fixture byte-unchanged assert) and one
live `bash tools/tsukuroi-census.sh` (read-only per its contract — md5 identical before/after,
`git status` byte-identical before/after, no `db.lck`), plus reads of `LOG.md`, `SCORECARD.md`,
`SHONEN.md`, `corpus/README.md`, `SKILL.md`, `plans/round-{2..10}*.md`, `corpus/knowledge/*.md`
(tsukuroi), and two read-only sibling notes for the cross-author sweep
(`tameshi-shokunin/corpus/knowledge/{mutation-case-tsukuroi-census,fleet-kill-rate-ledger}.md`).
No external site; no AUR RPC; no install/upgrade/remove/restart verb (`PROVINCE.md:16-17`).
verified-at: 2026-10-14 dispatch window 20:52–20:58Z; HEAD `fac745b` (round-9 commit); this
note is written by seat S10-1 and is that seat's only write.
recheck: §7 — re-hash every pin, re-run the selftest, re-read the cited sections; never quote
this note's captures.

## 0. Scope, rules, dispatch state

**0.1 What this note is.** The lane's calibration ledger for its first nine landed rounds
(LOG rounds 1–9; commit labels "probation round 1…9"). Calibration is the discernment axis of
`LEARNING.md:23-33,73-78`: the lane's ability to know which of its own statements are measured
and which are believed, and to correct the latter. This note records the measured-vs-believed
divergences the lane caught in its own work, the correction each produced, and the pattern
those corrections share. **It makes no new host claim**: every row cites a landed artifact
re-hashed at dispatch; plan-side statements are marked `[plan]` and never counted as landed.

**0.2 Rules and conventions** (each is itself a product of the pattern in §1):
- Tags `[observed]` / `[inference]` / `[unknown]` are kept separate, one per statement.
- A pin states its convention: `wc -l` vs a Read count; an **unterminated final line** makes a
  Read count `+1` (measured for the census and `SKILL.md`, round-9 record §3.3).
- Every count/verdict is a **capture** with a time; re-run, never quote (proof: the same
  coredump class reads 198 → 208/211/220/224 → 244 → 279 → 467 → 522 across rounds 1–9 on
  the same boot — every value a capture).
- A **moving revision** is observed shape-only; no pin is taken from it (post-freeze practice
  in `plans/round-9-record-draft.md` §8; reused here in 0.3).
- Errata are **append-only**: a corrected claim keeps its original text; the supersession is
  an appended block (`package-state-plane.md:228` heading "Errata / method corrections
  (append-only)" — the discipline, not an edit).

**0.3 Dispatch state [observed].** At 20:52:25Z `git status --short` = 0 lines; census md5
`e32aac98c6b54f9d7fb8bc4f348cd467` · sha256
`c396662eeb5f435d841b0c1863903dba807aa9dcbc6a67b2439fdfb13670c650` · 2349 `wc -l` · 123 410 B
before **and** after both runs. Own executed receipts: selftest rc=0 verbatim
`TSUKUROI_CENSUS_SELFTEST: PASS (74 cases, 74 passed, 0 failed)`; live rc=1 (census header
`2026-10-14T20:52:36Z`), **six** `PLANE` lines, rollup verbatim
`TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=HEALTHY)`;
`/var/lib/pacman/db.lck` absent. At 20:55:25Z the tree showed one sibling round-10 file
(`?? corpus/knowledge/census-closeout-receipt-r10.md`) — not read, no pin taken from it.

## 1. The correction pattern (the method)

Across nine rounds the lane's durable reliability did not come from being right first; it came
from a repeated five-step loop:

1. **Claim** — a measurement-time statement lands in a note, the gate, or a record (with its
   time, its command, its scope).
2. **Re-measure** — a later round, a mutation sweep, a non-author verifier, or the next gate
   revision re-runs the probe independently.
3. **Record the divergence append-only** — the new reading is appended as errata; the original
   text is never rewritten ("kept as method evidence", "recorded here, not rewritten",
   "recorded, not smoothed").
4. **Supersede the restatement** — the superseded number/claim stays visible where it stood;
   count restatements move together with any gate revision (rule live at `SKILL.md:925-929`,
   `:1147-1151`, `:1309-1316`, `:1372-1375`).
5. **Distil or name the gap** — if mechanical, a rule (and a selftest case that can fail);
   if not measurable read-only, an `[unknown]` with an owner — never a silent pass.

Two event kinds are ledger rows: **corrections** (a belief was wrong) and **confirmations**
(a belief survived independent re-measurement). Both are recorded; a confirmation of one's own
prior run is only a confirmation when the probe is independent (round-7 VER-S7 ran its own
probes; the round-9 probe receipts that "reproduce the plan's own receipts exactly" are marked
"expected, not independent confirmation", round-9 record §3.2).

The rules the pattern distilled, each provable from the ledger below:
- **capture-not-quote** (drift proof, §0.2/§4.3);
- **fail-closed** — an unreadable probe is `BLOCKED`/`unknown=`, never a pass (gate arms from
  round 2 on; e.g. `foreign=? [pacman -Qm unreadable]`, `SKILL.md:896-899`);
- **a case that cannot fail is not a case** — the local-name test for a fixture that cannot be
  made non-vacuous (round-9 plan `:125-126`, kept from round 5; realized at `SKILL.md:1290-1292`
  by making the channel stamp settable, so the case executed rather than being dropped);
- **a survivor is a finding, never a footnote** (`SKILL.md:611-617`);
- **kill-rate is bounded by composition** — two sweeps of one file are two pins, cited
  separately, never merged (`SKILL.md:705-706`; tameshi ledger §4 band note);
- **attested ≠ verified** — a verifier named in a log line is not an artifact (§5);
- **predictions stay in the record when wrong** (M01, §2/§4.2).

## 2. The ledger, round by round

Format: **believed** (claim + where) → **measured/corrected** (artifact + pin at dispatch) →
**landed as**. Pins are dispatch-window hashes (§8); all cited notes were re-hashed.

**Round 1** (commit `55b2186`) — first-pass notes, audited same round.
- believed: sync-db mtimes date arrival; `comm` of local dirs vs `pacman -Qq`; raw line counts
  are counts; snapshot coverage inferred from `snapper`/hooks.
- measured/corrected, appended to the notes (append-only):
  - `comm` reconciliation **invalid** — dirs are `name-version`, `-Qq` prints `name`
    (`package-state-plane.md:230-234`);
  - cache "age" from mtimes **wrong** — pacman preserves upstream mtimes; use `%w`/`%z`, proven
    by sync-db birth 2026-10-11 vs mtime 2026-09-08 (`:235-237`);
  - full `-Qkk` output needs `tr '\r' '\n'` normalization; later measured **necessary but not
    sufficient** — 6 summaries spliced by interleaved `warning:` output, 0 CR bytes in that run
    (`:238-239`, `:248-256`);
  - unit-file count **136 raw lines → 133 rows** (1 header + 133 + blank + footer)
    (`systemd-user-plane.md:204-208`);
  - **rollback-net inference retracted** — installed `snapper`/`limine-snapper-sync` + empty
    `snapper list-configs` ⇒ no rollback net configured ("kept as erratum, not laundered into
    the body", `package-state-plane.md:275-280`);
  - journal first-pass failed-pattern count **retracted** — the "1 line" was the
    `-- No entries --` notice counted by `wc -l`; corrected 0 strict / 36 broad
    (`journal-boot-plane.md:338-340`); plus two more method corrections (`NextElapseUSecMonotonic`
    is a timestamp, not a delta; UFW filter anchor `[UFW BLOCK]` → 8811) (`:341-345`);
  - the 18-vs-19 `-Qkk` sweep split **resolved by measurement** (fragment attribution;
    ≥19, no drift) (`package-state-plane.md:257-265`).
- landed as: errata blocks; `SCORECARD.md:12` names four of these ("sync-db mtime→birth,
  journal line→entry count, unit-file count 136→133, rollback-net inference retracted").

**Round 2** (commit `5f90645`) — the first executable gate.
- believed: the distill's quoted census md5 prefix was the settled file's md5.
- measured: SKILL quotes `7a3d3b94ed…`; the settled v1 file hashes `7a3d3b94ec…` — a
  **transcription candidate, recorded here, not rewritten** (`LOG.md:68-71`; carried visible
  through the round-5 errata, `SKILL.md:705-706`).
- landed as: the recording rule (a mismatch stays visible; a pin's convention is stated —
  v1 is "744 lines / 743 `wc -l` newlines", `corpus/README.md:11`).

**Round 3** (commit `9bcd162`) — freshness + depth; the round whose beliefs later needed most.
- believed: "**0 unit failures in 13 retained boots**" (`journal-boot-plane.md` §4 — the claim
  this synthesis treats in §3); the boot-gap explanation (var-log.mount delay) as an inference;
  the SKILL document was sufficient for a no-oral-context executor.
- measured:
  - boot-gap: kernel phase = first-record monotonic − 0.81…0.84 s (12/12 boots), wall-clock
    cross-anchor ±1 s; var-log.mount delay **refuted** (mount at userspace 2.845 s, after PID1
    logging starts); leading hypothesis initramfs/LUKS dwell, unproven, crypttab BLOCKED
    (`corpus/README.md:13`; `SCORECARD.md:14`);
  - no-oral-context test: per-step tally **7 SUFFICIENT / 3 PARTIAL / 3 MISSING** — the MISSING
    steps were exactly the census-v2 coverage (`executor-test-sufficiency.md`; `corpus/README.md:15`);
    fixes landed same round as the SKILL append (444 → 543 lines); **post-append re-test not yet
    run** (LOG.md:153-154; still owed at dispatch, §6);
  - mid-flight gate revision v1→v2 during the report's window — **recorded, not laundered**
    (`host-health-report-r3.md:408-412`, "recorded not laundered" in `corpus/README.md:14`);
  - "20-min cap" item **recorded as unresolved, not invented** (`executor-test-sufficiency.md` §7 U1);
  - stale figures re-measured instead of quoted (coredumps 198→208→211→220→224; err 247→251 in
    capture; every count a capture) (`SCORECARD.md:14`).
- landed as: the measured boot rule, the same-round SKILL fix, the open-item list.

**Round 4** (commit `165307f`) — depth (triage); the round that corrected round 3.
- believed (r3's, now re-measured): the failed-unit claim (→ 4 records, §3); sr0 LBA reads a
  closed noise floor; `failedhist` was 0; pipewire "active since boot"; the limine-snapper
  J4 claim was "self-claim vs empty configs".
- measured/corrected (`degraded-triage-r4.md` §9, `:567-583`):
  - sr0 **second burst** (115 lines) at 13:10–13:11 — r3's wording stands as written, the change
    is recorded;
  - `failedhist=8` at 16:19:56Z — **no unit failure occurred**; the census arm fires on
    `systemd-xdg-autostart-generator` "Failed to create unit file" collisions (arm semantics
    measured: `CLASS_FAILED` counts failure *messages*, not failed units — the journal arm's
    meaning is documented, `SKILL.md:483-507`);
  - pipewire erratum superseded (both units re-entered active 13:11:08, NRestarts=0);
  - J4 **reframed**: the measured truth is a failed auto-init (EACCES) — "the claim was an
    attempt, not a false statement";
  - boot-plane `§8` errata: the round-4 recheck table said "13 boot rows" for a `wc -l` that
    reads **14** (header + 13) — row-count vs line-count conflation, corrected
    (`boot-plane.md:302-311`);
  - own first-pass method error kept: `jq '.[]…'` without `-s` on json-lines errored every line
    (`boot-plane.md:225-227`).
- verification: **VER-S1** — "P1/D2/U6 CONFIRMED, 755-not-644 correction" (`LOG.md:167`); no
  landed VER-S1 artifact exists in the tree (§5, §6 resolves the unrecoverable half).
- landed as: triage note + errata blocks; the r3 claim's supersession pointer was added to
  `journal-boot-plane.md` §13 (`:416-425`), which also measured that `corpus/README.md:13`
  **still repeats the stale claim** (still true at dispatch — §6).

**Round 5** (commit `da95290`) — adjacency (own-gate mutation) + freshness.
- believed: the own suite covered its own arms.
- measured — own sweep of the 976-line/26-case revision (`41953ee9…` md5 · `084951be…` sha256, committed):
  **23 defects → 13 killed / 10 survived (57%)**; survivors in three families (fail-closed arms
  with no fixture; counts never asserted nonzero/exact; boundary/unknown semantics)
  (`SKILL.md:558-592`). Hardening: 9 new cases (26 → **35**); same defect set re-swept
  **23/23 killed** (`SKILL.md:594-609`). Adjudication rules pinned (killed = suite red **and**
  the full case count still enumerated; inconclusive excluded and named; kill-rate =
  killed/(killed+survived)) (`SKILL.md:611-617`).
- cross-author re-measurement (tameshi, same revision, own 10-defect set, pre-registered):
  **6 killed / 4 survived (60%)**; after the owner's hardening, replay of its 4 survivors:
  **B10 killed, B7/B8/B9 still survived — 1/4 closed** (`tameshi-shokunin/.../fleet-kill-rate-ledger.md`;
  `mutation-case-tsukuroi-census.md` §1). Two sweeps of one file = two pins, never merged; a
  100% rate on one set is not suite completeness (`SKILL.md:705-706`).
- substrate incident I1 [observed, recorded not smoothed]: the census moved mid-sweep by a
  concurrent lane; tameshi re-pinned before/after and refused the stability claim it could not
  make (`mutation-case-tsukuroi-census.md` §I1). This is the ancestor of the "no pin from a
  moving revision" rule (0.2).
- landed as: gate hardening + the kill-rate ledger in SKILL; timer-drift plane.

**Round 6** (commit `dc3436d`) — coverage + freshness (AUR risk; OOM-event plane).
- believed: the kernel ring's `oom=1` reading describes the OOM class; the 16 foreign packages'
  provenance questions could rest on earlier notes.
- measured:
  - the OOM-event plane's own blind spot: event B (13:10:59 teardown) has **0 kernel records**
    while the census's kernel `oom` arm reads 1 — C2 (systemd attribution) added to the
    detection contract, with the rule "the two must be reported together"
    (`oom-event-plane.md` §8; the C1–C6 vocabulary later becomes the census arm's `mem=` fields);
  - C4 cgroup reads are **presence flags, never meters** (round-6 rule, kept in the arm);
  - foreign provenance re-measured per-package (`foreign-provenance-r6.md`); VER-S6 verified
    the register's channel claims from its own probes: **CONFIRMED, 2/2 rows; 0 claims refuted;
    2 documentation deltas, 1 live-drift noted** (`aur-risk-plane-ver-s6.md:15`).
- landed as: the AUR-risk register + OOM vocabulary; the round-6 named debts (baseline file —
  later landed as an embedded baseline, not a `.tsv`).

**Round 7** (commit `aa136d6`) — the watch arms land.
- believed: the plan's claim (a) (fifth plane) and claim (b) (r2 errata pointer) were in scope
  for the round.
- measured: neither was in the tree at append time — both **tagged not landed and carried**,
  never silently dropped (`SKILL.md:844-846`); the foreign watch's fail-closed branches were
  independently verified by **VER-S7: CONFIRMED** — count and fold reproduce from the verifier's
  own probes; all four fail-closed branches fire and name their class
  (`aur-risk-plane-ver-s7.md:23`; `SKILL.md:900-903`).
- self-named gap (**AUD-X7**): S7-2's memory arm has **no non-author verification** — queued,
  recorded in the round's own log row (`LOG.md:170`).
- landed as: census revision (49 cases = 35 legacy + 6 foreign-baseline + 8 memory-arm,
  `SKILL.md:866-869`), the v2 decision note, and an open verification debt with a name.

**Round 8** (commit `72b038d`) — the verification round.
- believed: S8-1's 11-mutant set described the arm's kill power; the verifier's own 16-defect
  predictions.
- measured (`memory-arm-ver-s8.md`):
  - replay of S8-1's 11 mutants **byte-for-byte identical** (same sha256s, same verdicts,
    same per-case attribution): D1–D8 kill their owning cases, D9–D11 survive; **AUD-X7 closed**
    with verdict `CONFIRMED` (`:90-103`, `:105-114`; `LOG.md:171`);
  - own complementary set (16 defects, pre-registered): **11 killed / 5 survived (69%)**;
    **prediction score 15/16 — M01 was predicted SURVIVED and was killed**; mechanism measured:
    the stub dispatcher routes C1 by literal `--grep oom_reaper` pattern, so the kill was a
    **routing coupling, not a semantic assertion** — "recorded as a prediction error, not
    smoothed" (`:170-176`);
  - consolidated coverage debt: **9 clause sites un-exercised by the 49-case suite**
    (S8-1's D9/D10/D11 + own M04/M06/M10/M12/M15 + supplementary M17) (`:177-181`); a 15-case
    independent fail-closed battery caught every survivor — "the debt is suite coverage, not
    undetectable semantics" (`:149-166`);
  - method delta vs S8-1 recorded (byte copy vs repo file; identical mutant bytes prove the
    same instrument outcome) (`:188-190`);
  - the plan's `PLANE oom` + baseline rows were **unverifiable at the pin** → carried, owner
    named, not re-opened (`:182-187`).
- landed as: VER-S8 note + mutant set + kill-event depth note; LOG row naming the closure.

**Round 9** (commit `fac745b`) — the 5-plane→6-plane round; landed in two steps.
- believed/lands: the update-safety plane (S9-1) first — 5 planes, 63 cases
  (revision `0f72f4cf…`, 2011 `wc -l` at the append's write time, uncommitted then,
  `SKILL.md:1320-1323`); then the oom plane (S9-2) landed on top — 6 planes, 74 cases,
  revision `e32aac98…` (2349 `wc -l`, 123 410 B) (`SKILL.md:1345-1371`).
- measured/recorded:
  - the pin move is an **append-only addendum with the mismatch named** — "this is that
    mismatch, recorded, not smoothed" (`SKILL.md:1352-1356`); count restatements re-moved
    49 → 63 → 74 (`:1372-1375`); the earlier append's caveat ("a later re-hash mismatch means
    the gate moved again — re-hash first") is exactly what happened (`:1320-1323`);
  - update-safety fixtures: 14 `(R9)` fail-closed cases with realized labels; the named
    `[design]` prerequisite was **realized, not dropped** — the channel stamp is the fixture
    db's own mtime, settable with `touch -d`, so the stale-channel case executes rather than
    being claimed vacuous (`SKILL.md:1278-1297`);
  - AUR watch's first drift receipt is an **explicit no-drift** (foreign=16 known=16 new=0
    drift=0 gone=0, confirmed three ways) — and the note separates "no drift" from "current or
    safe" (`aur-drift-receipt-r9.md`; `SKILL.md:1299-1307`);
  - this seat's dispatch run re-executed the landed revision: 74/74 selftest, six-plane live
    rollup, zero mutation (0.3).
- open at dispatch: the r9 LOG row is a one-line compression whose precision is imperfect
  (§6); no VER-S9/S9 lesson artifact landed (§5–6).

## 3. Worked example — round 3's "zero unit failures", refuted in round 4

The lane's clearest self-correction, end to end:

1. **Claim (r3).** `journal-boot-plane.md` §4: "zero unit-activation failures in 13 retained
   boots" — read via the note's failed-pattern sweep; the claim also rode into the corpus index
   (`corpus/README.md:13` still carries it at dispatch).
2. **Why it was wrong (measured in r4, `boot-plane.md:217-224`).** Two filter defects: the
   strict pattern `failed with result` is **lowercase** while systemd logs `Failed with result`;
   and the broad set **excluded `Failed to enqueue`**. Re-measurement with case-insensitive
   patterns found **4 failure records**:
   `elephant.service` exit-code (boot −2), `app-com.onepassword…@autostart.service` core-dump
   (boot −1), `app-Hyprland-xdg-terminal-exec…scope` oom-kill (boot 0),
   **`user@1000.service` signal (boot 0, logged by PID 1)** (`boot-plane.md:99-102`).
3. **Recorded append-only.** `boot-plane.md` §5 supersedes the claim and states the root cause;
   the original note is **not edited** ("append-only discipline"); `journal-boot-plane.md` §13
   later added the missing pointer (`:416-425`) and measured the stale README row it cannot
   edit (outside that seat's write scope).
4. **Restatement discipline.** The superseded figure stays visible; the README row is named as
   debt, not silently fixed (still unpaid at dispatch — `corpus/README.md:13` unchanged since
   round 3, `98bd0066…`).
5. **Distilled.** The gate's journal arm and the "failed units" concept stay explicitly
   separate: today's `failedhist=8` are generator-collision messages, not failed units
   (`degraded-triage-r4.md:573-576`), and the r9 live run still prints `failedhist=8` — the arm
   means "failure-message history", documented rather than conflated.

This example is the pattern's whole arc in one item: claim → independent re-measurement →
append-only correction → supersession left visible → concept split made explicit — and it also
proves the meta-rule that **a correction propagates one level slower than the claim** (the note
was fixed in substance in r4; the index row is still stale in r9's tree).

## 4. The census's own accuracy history

The gate is the lane's most self-measured artifact. Its history is a chain of revisions, each
with its own accuracy events; identity is **by hash, not version string** (banner stays
`census-v2`) (round-5 rule kept, `SKILL.md:863-864`).

**4.1 Revision table** (dispatch pins; line counts `wc -l`; unterminated final line untested for
v1/v2 — stated as unknown where not re-read):

| rev | pin (md5) | lines | cases | planes | accuracy event |
|---|---|---|---|---|---|
| v1 (r2) | `7a3d3b94ecd73fbe1a9a98e9dc88b92f` | 744 / 743 `wc -l` | 17 | 3 | md5-prefix transcription candidate recorded, not rewritten (`LOG.md:68-71`) |
| v2 (r3) | `41953ee9f2099281c91759249fe8708f` | 976 | 26 | 4 | journal joins; `coredumpctl` deliberately not probed (table-parse trap); kernel double-count declared with its distinct value (`corpus/README.md:12`) |
| hardened (r5) | `e9327046b05b5c71e07fe511ad7e82dd` · sha `aae45531…` | 1032 | 35 | 4 | mutation: 13/23 → hardening → 23/23; cross-author replay 1/4 closed (`SKILL.md:594-609`, tameshi ledger) |
| r7 | `e2c4558a3ae4ddd2eca67e8f4d64281c` · sha `bba6cdf6…` | 1472 | 49 | 4 | two new arms; VER-S7 CONFIRMED; AUD-X7 self-named |
| r9a | `0f72f4cf…` (uncommitted at append) | 2011 | 63 | 5 | update-safety plane; 14 (R9) fail-closed cases; prerequisite realized |
| r9b (HEAD) | `e32aac98c6b54f9d7fb8bc4f348cd467` · sha `c396662e…` | 2349 | 74 | 6 | pin move recorded in append-only addendum; count restatements re-moved 49→63→74 |

Case-count history, restated as one line: **17 → 26 → 35 → 49 → 63 → 74**. A gate revision
moves every restatement with it (rule live at `SKILL.md:925-929`, `:1147-1151`, `:1309-1316`,
`:1372-1375`). Dispatch executed receipt: 74/74 rc=0; six-plane live rollup rc=1 (0.3).

**4.2 The gate's own accuracy under attack** (all figures from the cited notes):
- owner sweep r5: 13 killed / 10 survived (57%) on the 26-case revision; after hardening,
  23/23 (100%) **on that same defect set**;
- cross-author (tameshi) r5: 6/10 (60%) on the same revision; after the owner's hardening,
  replay of its four survivor probes: **1/4 closed** — i.e., a different author's mutants found
  clause gaps the owner's own 100% re-sweep could not see;
- r8: replayed 8/8 owning-case kills; **9 clause sites named as un-exercised by the then-49-case
  suite**; a 15-case battery demonstrated each is detectable (coverage debt, not unknown
  semantics); one verifier prediction was wrong (M01) and stays in the record;
- disposition of the residual survivors: tameshi's B7/B8/B9 have **no landed closure** through
  round 9 (§6).

**4.3 Captures, not quotes** (the drift proof). The coredump class (same boot, same host):
198 (round 1) → 208/211/220/224 (round 3) → 244 (round 4) → 269 (round 6) → 279 → 467
(round 9, 48 min apart) → 522 (r9 live line) → and the round-1 scribe's `kerr=38` vs round-4's
`137` vs round-9's `139`; foreign=16 stable across rounds but still a capture. The gate's
arm-identity rule generalizes this: equal readings are captures too, never confirmations.

**4.4 What the census never claimed** (as important as what it did):
- no standalone baseline file: the register's proposed `.tsv` **stayed a proposal**; the
  baseline is embedded (`base=r6(16)`) and an absent baseline must degrade, never pass
  (`SKILL.md:891-899`);
- the version string is not identity; `--sample` default 8 is a cap, not a count;
- `coredumpctl` is deliberately not probed (table parsing measured as a trap);
- zero mutation, every revision: live mode writes nothing, the suite asserts the fixture
  byte-unchanged, `git status` byte-identical before/after, no `db.lck` (r2→r9 receipts;
  re-verified at this dispatch, 0.3);
- read-only means read-only: no transaction, no download, no db write — `-Qu` unpiped so its
  rc is the command's own (`SKILL.md:1233`; r9 record §3.2).

## 5. The verification ledger — artifact vs attestation

**Landed and re-readable** (dispatch pins):
- `aur-risk-plane-ver-s6.md` `b0de352dec653891d5d36dd742536198` (133) — VER-S6: **CONFIRMED
  2/2 rows, 0 claims refuted, 2 documentation deltas, 1 live-drift noted** (`:15`);
- `aur-risk-plane-ver-s7.md` `4608743dfa6230e806985d164f3c00f4` (184) — VER-S7: **CONFIRMED**
  (count + fold reproduce; all four fail-closed branches fire) (`:23`);
- `memory-arm-ver-s8.md` `861d83ad5a120487507b167236ee3cd0` (251) + its mutant set
  `memory-arm-mutants-s8.md` `a09e5604a9a818f38096569365d48823` (181) — VER-S8: AUD-X7 closed,
  with its own prediction error and debt list kept.

**Named in log rows but not landed as files** [observed: `find` over the tree finds no
`*ver-s1*`/`*ver-s9*`/`*aud*` file; `git log --diff-filter=D` is empty, so nothing was
deleted — they never landed]:
- VER-S1 (round 4; `LOG.md:167`), AUD-S5 (round 5), AUD-S6 (round 6), AUD-S9 and VER-S9
  (round 9; `LOG.md:172`). ERR-S (round 4) is artifact-backed via the errata blocks it swept
  into (`boot-plane.md:302-311`, `journal-boot-plane.md:414-425`).
Consequence, stated as the rule the ledger earned: **a verifier named in a log line is an
attestation; only a landed note is a verification a later round can re-read.** The round-9
record itself states the same for its plane (a non-author verification "is a separate active
seat's product and is quoted when it lands, never anticipated here", `SKILL.md:1333-1336`),
and the round-10 plan [plan] states the standing rule `attested ≠ verified` (D13). The triage's
own §8 spot-checks (settled by arithmetic and sha256 closure, `degraded-triage-r4.md:551-566`)
are **internal** re-derivations — valuable, but author evidence.

## 6. Open calibration debt (things this ledger cannot close)

1. **"755-not-644 correction"** (`LOG.md:167`, round 4) — [unknown]. No landed artifact decodes
   the correction's antecedent reading; the only landed "755" readings are
   `degraded-triage-r4.md:414` (`omarchy-restart-walker`, mode 755 vgpnk:vgpnk, 709 B) and
   `update-safety-note.md:236` (709 B, mode 755). The "644" first-pass reading is not
   re-derivable from the tree; the log row is the only witness. Owner: the r4 archival seat
   (or the operator's wave-4 dispatch records, outside this lane).
2. **Round-9 LOG row precision** — the one-line row reads "the 5-plane census landed
   (update-safety arms — the r7 AUD-X7 gap closed; PLANE oom)" (`LOG.md:172`). The landed gate
   emits **six** planes / 74 cases (`SKILL.md:1345-1363`), and AUD-X7 was closed by round 8's
   VER-S8 on the **memory** arm (`LOG.md:171`), not by round 9's update-safety arms. The row is
   a compression; recorded here as a precision observation — the row itself is not edited
   (append-only).
3. **tameshi survivors B7/B8/B9** — no landed closure; the r8 mutant work targeted the memory
   arm's clauses (its §7 states the other planes' arms were exercised only as the suite's
   41 non-S7-2 cases). Owner: a future gate hardening round.
4. **Post-append no-oral-context re-test** — owed since round 3 (`LOG.md:153-154`; `SHONEN.md`
   box 3 says "post-append re-test not yet run"); still not landed at dispatch. The belief "the
   corrected document is sufficient" remains **untested**.
5. **`corpus/lessons/` = 0 files** [observed, dir empty at 20:53Z] — the discernment loop's
   contracted home (`LEARNING.md:37-43,61`) has never been written; the round-9 record named
   round-9's own lesson as "the lane's first" and it did not land. No retro-fabrication is
   proposed here: a Gate for rounds 1–8 would invent decisions (round-9 record §8 boundary).
6. **Index/row debts that keep superseded claims visible**: `corpus/README.md:13` still repeats
   "0 unit failures in 13 retained boots" (measured stale in round 4, `journal-boot-plane.md:424-427`);
   the whole README is unchanged since round 3 (`98bd0066…`, 20 `wc -l`; last touched `9bcd162`),
   so rounds 3–9 coverage rows are owed; `SCORECARD.md:16` (round-4 row) is malformed —
   the unescaped `|` truncates it to `boot plane (299 L` [observed at dispatch].
7. **Carried, unchanged** (calibration-relevant subset): the r2 errata pointer
   (`update-safety-note.md` unchanged `5cc3067f…`); root `-Qkk` delta; `offline.db` coverage;
   the "20-min cap" item (owner: integrator); the upstream Arch/omarchy delta — the real
   update gate — stays `[unknown]` read-only (the 36 d stamp is a capture).

## 7. Recheck set (read-only; run from the lane root)

```bash
md5sum tools/tsukuroi-census.sh                     # expect e32aac98c6b54f9d7fb8bc4f348cd467 (a mismatch = re-read §4.1 first)
bash tools/tsukuroi-census.sh --selftest            # expect rc=0, PASS (74 cases, 74 passed, 0 failed)
bash tools/tsukuroi-census.sh                       # expect rc=1, six PLANE lines, rollup with oom=HEALTHY
git status --short                                  # zero-mutation receipt: identical before/after both runs
md5sum SKILL.md LOG.md SCORECARD.md corpus/README.md SHONEN.md   # dispatch pins in §8
sed -n '13p' corpus/README.md                       # the stale row this ledger names (claim vs index)
sed -n '16p' SCORECARD.md                           # the malformed r4 row
ls corpus/lessons/                                  # 0 files = the discernment ledger is still empty
md5sum corpus/knowledge/boot-plane.md corpus/knowledge/journal-boot-plane.md \
  corpus/knowledge/degraded-triage-r4.md corpus/knowledge/memory-arm-ver-s8.md
grep -n "AUD-X7\|sweep" LOG.md                      # the one-line rows §6 examines
```

Rules restated for the re-run: unpiped rcs only; an unreadable probe is `BLOCKED`, never a
pass; every number is a capture with a time; no pin from a moving revision.

## 8. Dispatch pins and erratum

All pins below are `md5` re-hashed 2026-10-14 20:52–20:58Z against a clean tree
(`git status --short` = 0 lines at 20:52:25Z; HEAD `fac745b`); line counts are `wc -l`.

| artifact | md5 | lines |
|---|---|---|
| `tools/tsukuroi-census.sh` (r9b, 6-plane; sha256 §0.3) | `e32aac98c6b54f9d7fb8bc4f348cd467` | 2349 · 123 410 B |
| `SKILL.md` | `d276ecea1b1abaf5d6bbf6a6d7e31746` | 1374 |
| `LOG.md` | `68413998f6770e8b85ed88e5d8c693d3` | 172 |
| `SCORECARD.md` | `da962e185f874e4686d92ab21a58572a` | 21 |
| `SHONEN.md` | `9cf1d450685ae0ed0d15dee1b54e8fd5` | 51 |
| `corpus/README.md` | `98bd00668e84f18cf6781718c4d09ea0` | 20 |
| `boot-plane.md` / `journal-boot-plane.md` | `e722b7a931858aa5ff1a89ce91cccca9` / `e5ca40dafc4d1d2a2158fded39067df6` | 312 / 430 |
| `degraded-triage-r4.md` / `host-health-report-r3.md` | `d57ae2d48e01777e1ef3c8c0ffb642c9` / `98a0f263f801245f6069e57a9f72d4af` | 607 / 563 |
| `executor-test-sufficiency.md` / `package-state-plane.md` | `4b2c1d3612db7db1477da92aaec39862` / `ef93f1b78b6a9e17e8c9d096e7852a02` | 219 / 323 |
| `systemd-user-plane.md` / `driver-firmware-plane.md` | `af07a829cfd0307fbe970a2cdc054e18` / `518eda8f0f39f25ee95c715571a9cf95` | 265 / 256 |
| `memory-arm-ver-s8.md` / `memory-arm-mutants-s8.md` | `861d83ad5a120487507b167236ee3cd0` / `a09e5604a9a818f38096569365d48823` | 251 / 181 |
| `aur-risk-plane-ver-s6.md` / `aur-risk-plane-ver-s7.md` | `b0de352dec653891d5d36dd742536198` / `4608743dfa6230e806985d164f3c00f4` | 133 / 184 |
| `oom-event-plane.md` / `kill-event-deep-r8.md` | `7e99d712ead088727c0980e52a121199` / `6685e1da443f5d368cd41584d2b9943e` | 433 / 340 |
| `aur-drift-receipt-r9.md` / `foreign-provenance-r6.md` | `e7d6f70b65e4846ad7001b5a66e8ec73` / `1b8f47a2a807fc8bd2fc7302f15577c8` | 248 / 307 |
| `update-safety-note.md` / `update-safety-v2.md` / `update-safety-v3.md` | `5cc3067fec33d261d8bff6a5c7e8ac48` / `92803aea74ebeb1598fa4f450489e5d2` / `2ac0c21db678c1c806d6de9e546daf2e` | 478 / 353 / 387 |
| `plans/round-4.plan.md` / `plans/round-5.plan.md` [plan] | `63c26bb14d59126cd24de8255dda2fc4` / `0e9e8640e8c6b1d2fd116d05c5acf19b` | 10 / 11 |
| `plans/round-9-record-draft.md` | `b5d6681e77702e20ee0f5d5bdbf52ca5` | 537 |
| tameshi `fleet-kill-rate-ledger.md` / `mutation-case-tsukuroi-census.md` (sibling, read-only) | `a0df7d76d839244c6b6a9286f2d10c9a` / `0af391efed0879a09baa684e2935619d` | 363 / 396 |

- 2026-10-14 — this note created (seat S10-1, round 10). It is a synthesis of landed
  artifacts only; its own line count and md5 are reported in the seat's handoff, not in-file
  (a further edit would invalidate them — round-9 record precedent). All fix-ups stay
  append-only below this line.
- 2026-10-14 — scope note: the round-10 plan's draft name for this synthesis
  (`plans/round-10.plan.md`, `corpus/knowledge/ten-round-synthesis.md`) was superseded by the
  assignment's realized name, `corpus/knowledge/calibration-synthesis.md`; the landed name wins.
- 2026-10-14 — moving-tree observation (shape only): at 20:55:25Z the tree gained
  `?? corpus/knowledge/census-closeout-receipt-r10.md` (a sibling round-10 seat's file) —
  content not read, no pin taken. The census remained `e32aac98…` throughout this seat's runs.
- 2026-10-14 — post-write shape movement (append-only, shape only): by 20:58:34Z the tree also
  showed `?? plans/round-10-record-draft.md` and `?? plans/round-11.plan.md` (sibling seats'
  drafts — contents not read, no pins taken). All §8 hashes were re-checked at 20:58:34Z and
  are unchanged (census `e32aac98…`, `SKILL.md` `d276ecea…`, `LOG.md` `68413998…`,
  `SCORECARD.md` `da962e18…`, `corpus/README.md` `98bd0066…`, `SHONEN.md` `9cf1d450…`);
  `/var/lib/pacman/db.lck` absent.