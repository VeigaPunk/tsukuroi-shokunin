# ConnClaimSizing — Item X-4: round-38 declaration vs fleet claim-sizing rules

VERDICT: supports

Seat item: check the round-38 declaration (SCORECARD.md:2107–2131, freeze commit
`7cbaeb6317cb9f7323d2619eec02db4e4da29449`, pre-seat amendment `9c9bb6477951b3a52ac49ed83db4395765dfcf1a`)
against each bullet of the fleet claim-sizing rules (`.ufo/prompts/tsukuroi-round-38.md:439-461`, bullet 9) and
against the rejection patterns of `corpus/lessons/round-3{4,5,6,7}-verifier-spotcheck.md`. All commands run
read-only against the lane on 2026-10-26. No installs, no clones, no scratch (no fixtures or mutants were built;
nothing to clean).

## 0. Anchors verified

- `git merge-base --is-ancestor` for `7cbaeb63`, `9c9bb64`, `52ffd65f868431f021b8615ab281efd87195eac6`,
  `1fe28e725be47364fc6033bf81ecabc66ee5fe62` against master → all ancestors (freeze-ok / amend-ok / impl-c1-ok /
  impl-c2-ok).
- The declaration section is inside the freeze commit itself:
  `git show 7cbaeb63:SCORECARD.md | grep -n 'Round 38 — declaration'` → line 2107 (the section the assignment
  cites). `git show 8bd001f:SCORECARD.md | grep -c 'Round 38'` → 0, so the declaration postdates base, as claimed.
- Freeze-commit timestamps: author Sun Oct 25 17:06:38 -03:00, **committer Mon Oct 26 01:16:08 -03:00
  (04:16:08Z)** — equal to the heading stamp `2026-10-26T04:16Z`. Amendment author/committer Oct 26 01:32:13
  -03:00 (04:32:13Z) — equal to its `04:32Z` heading. On-disk receipt mtimes (01:11/01:29/01:31 local) precede
  their commits. The rounds-34/35/36 evidence-timing class is checked and **not** carried in the declaration.

## 1. Bullet-by-bullet conformance

### B1 — one concrete after-state, re-derivable with one command over committed bytes, sized to one round: MET

- C1 predicate is the same sentence in plan (SCORECARD.md:2117), counter code
  (`tools/score-storage-arm-r38.py:7` docstring, `:230-232` verdict/`predicate` field) and receipts
  (`.ufo/waves/round-38/after/c1-after-52ffd65.json` `"predicate": "fixtures_matched == FIXTURES_EXPECTED and
  live_match == 1 and six_planes_all == 1"`, result PASS 10/10, live 1, six_planes_all 1, exit 0). Before receipt
  `before/c1-before.json` reads the same fields FAIL at base `8bd001f`.
- C2 likewise: `tools/check-hook-order-r38.py:8` and `:207` carry
  `rows_expected == rows_matched and mismatches == 0 and extra_rows == 0 and source_ok == 1`;
  `after/c2-after-1fe28e7.json` reads 69/69/0/0/1 PASS at `1fe28e7`; `before/c2-before.json` reads 0/69,
  source_ok 0 FAIL at base. Input pinned: `sha256sum .ufo/waves/round-38/frozen/hooks-capture/MANIFEST.sha256`
  → `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`, matching the declared pin; capture holds
  67 + 3 = 70 hook files (69 effective, as declared).
- Sized to one round: C1 is one census arm (`probe_storage_arm`, `tools/tsukuroi-census.sh:1832`) plus six
  selftest cases (`storage-absent/-zero/-nonzero/-malformed/-duplicate/-no-devinfo`, `:2873-2919`); C2 is one
  knowledge entry (`corpus/knowledge/pacman-hook-order-r38.md`, HO1–HO7 at :21-27) plus one counter.
- Caveat (not a miss): after the amendment, C1's after-state is a conjunction across **two** frozen counters
  (v1 + Q82) plus the selftest kill conjunct — "one command" becomes one command per frozen predicate. Both live
  legs (sysfs read; `unshare -rm` bind over `/sys/fs/btrfs`) are disclosed host-dependent legs, and Q82 makes the
  namespace requirement claim-visible via `ns_available == 1` (`tools/score-storage-arm-r38-q82.py:18,132-133`).

### B2 — no universal clauses unless the counting command enumerates the full set: MET

Scan of SCORECARD.md:2107-2150. Every quantified clause is over an enumerated set: "six PLANE lines in every
run" (the counter enumerates the runs: 10 fixtures + 1 live); the kill rules are "Any of:" lists over counter
outputs; HO1–HO7 is a fixed 7-row set; selftest kill conjunct is the concrete count "0 failed"; "69 effective
hooks from 70 files" is a counted set (verified above). No "all/complete/every/no harm anywhere" claim appears
without its enumerating command. The no-harm conjunct is scoped to `--selftest` PASS at the measured revision,
not a universal.

### B3 — a calibration claim must count mismatches, not assert: NOT APPLICABLE

No calibration claim is declared; the declaration states "no self-assessment count is claimed this round"
(SCORECARD.md:2124). The round-37 C3 moving-snapshot failure mode is answered by abstention plus a
measured revision "declared before the after-run" (:2124).

### B4 — prefer 2 claims: MET

Exactly two claims in the table (SCORECARD.md:2117-2118); no third.

### B5 — never narrow a target after landing: MET

The only post-freeze rule change is the pre-seat amendment (`9c9bb64`, heading SCORECARD.md:2133 "tightening
only; no wave seat had scored"). `git show --stat 9c9bb64` → 252 insertions, 0 deletions over 6 files
(SCORECARD.md +31/−0; q82 counter added; q82 controls + novelty sweep added). It adds kill conditions only (Q82
conjunct for C1; per-row HO verdicts for C2), keeps the v1 predicates frozen, and every added condition points
toward not-verified — none converts a fail into a pass. Timing caveat is recorded under B6 and §2.

### B6 — a do-nothing control cannot reach the target; cheapest skip-work control built before freezing and receipted: MET, WITH ONE DISCLOSED DEVIATION

Freeze-time controls were committed in the freeze commit itself (`git show --stat 7cbaeb63` lists
`before/`, `controls/run-controls.sh`, `controls/controls.jsonl`, `frozen/hooks-capture/`), and observed values
match the declaration text byte-for-byte:

- C1 (`controls/controls.jsonl`): do-nothing 0/10 FAIL; constant `HEALTHY 1/1/0` emitter 2/10 FAIL; naive
  nonzero-digit emitter 6/10 FAIL (six_planes_all 0).
- C2 (`controls/controls.jsonl`): do-nothing 0/69 FAIL; plain full-name sort 63/69 FAIL; override-ignored 66/69
  FAIL; correct table without sourced row FAIL (source_ok 0); correct table with sourced row PASS — proving the
  counter can pass and that the table conjunct measures the order rule, not reading.
- Script hashes match the frozen pins: `sha256sum controls/run-controls.sh` → `cba1bec2…` (declared
  `cba1bec2c3e4130707c2d42e6dfebb0581cc2e23b369e84158b6e054fbfaf3ad`); `run-controls-q82.sh` → `5469e59a…`
  (declared `5469e59a5474881a2575a2f122e1bf278ea0c8e46ff925843dd494a634e4f5d6`).

Deviation: the mechanism-level skip-work control for C1 — a fixture-gated arm — was **not** in the freeze-time
set. It was built after the v1 after-receipts existed and is receipted in the amendment
(`controls/controls-q82.jsonl`: fixture-gated arm scores **v1 PASS 10/10, live 1**; under the added Q82 counter
it reads 0/3 FAIL; cached-live 1/3 FAIL; real arm at `52ffd65` 3/3 PASS). The lane followed the bullet's
prescribed remedy (counter wrong → fix before data) but strictly "before data" was violated: the disclosure says
"Read after the freeze and after the author's own after-receipts" (SCORECARD.md:2135). It is disclosed as a v1
counter defect, not hidden — "reported as a counter defect, not hidden" (:2137). Net state conforms: no control
meets either target under the frozen counters as amended.

### B7 — judged on the counter, kill rule and predicate declared before data; one predicate sentence in plan, code and receipt: MET

- Counter bytes equal the frozen shas at freeze and at HEAD: `sha256sum tools/score-storage-arm-r38.py` →
  `e649bfb3…82218` (frozen `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`);
  `tools/check-hook-order-r38.py` → `60e3635b…d1a8` (frozen match); `git show 7cbaeb63:…` for both gives the
  same shas; `tools/score-storage-arm-r38-q82.py` → `a183ff58…99e3` (frozen match, at `9c9bb64` and HEAD).
- Edit history clean: `git log --oneline 7cbaeb63..master -- tools/score-storage-arm-r38.py
  tools/score-storage-arm-r38-q82.py tools/check-hook-order-r38.py` → only `9c9bb64` (adds q82; the two v1
  counters untouched since freeze). This is the direct repair of round-37 routed defect 2 (counter amended after
  the change commit, no freeze sha).
- Predicate sentences byte-identical across plan/code/receipts (grep evidence in B1).
- Watch item (evidence, not claim text): the author after-receipts name revisions `52ffd65`/`1fe28e7` while the
  branch tip is now `5edb6c2`; the Q82 after-run at tip `5edb6c2` exists only as wave-seat output
  (`.ufo/waves/round-38/w1/Q82Rerun.md`, VERDICT: supports), and `git status --porcelain` shows `after/`, `w1/`,
  `l1/`, `assimilation/` still untracked. If these are not committed before filing, the closure will read the
  amended C1 predicate as unreceipted — the rounds-34/35 "unreceipted claim / post-filing leftovers" class.

### B8 — axis named by the surface; coverage names the surface moved and the unmoved command: MET

- C1 is named by surface, not number: "Storage integrity (btrfs per-device error counters) moves Frontier →
  Core" (SCORECARD.md:2117), against the held frontier rule quoted verbatim at `corpus/README.md:243` ("it
  becomes Core only after a read-only census arm reads it"). The unmoved command is the frozen counter at base:
  `before/c1-before.json` FAIL with the arm absent — `git show 8bd001f:tools/tsukuroi-census.sh | grep -c
  probe_storage_arm` → 0, at master → 2; `git diff --name-only 8bd001f master -- tools/` lists only
  `tsukuroi-census.sh` and the three round-38 counters. Sequencing note: the arm landed at `52ffd65`, so a
  closure re-run at base/mid-round revisions sees the arm appear mid-round — the before receipt at base is the
  honest unmoved witness.
- C2 is named by surface: "Update-safety plane: the host's effective ALPM hook order … the lane held only
  'override' and 'HookDir precedence' (S007/S008), not the order rule" (SCORECARD.md:2118). It is not
  re-scoring a held rule and not sourceless-fixture row counting: the novelty sweep as facts
  (`before/c2-novelty-sweep.txt`: 0 base hits for `ignores the suffix`, `_alpm_hook_cmp`,
  `TRANS_HOOK_FAILED`, `AbortOnFail`, `hookdirs`, `alphabetical order`, …; the 11 `transaction completed` hits
  shown to be pacman.log line quotes), and the C2-no-source control (69/69, source_ok 0, FAIL) proves the table
  alone cannot pass without the sourced rows.

## 2. Rejection patterns of rounds 34–37 still carried by the round-38 claims

Named per the item; "still carried" is answered per pattern.

1. **Counter-gameability discovered after after-receipts (r34: MutAttrgetterCopy/MutPathCopy met the frozen
   counter; r35: W2TreeKeyed/W2LogKeyed met VERSION 2) — CARRIED IN SEQUENCE, honestly handled.** The
   fixture-gated arm scored v1 PASS 10/10 live 1 **after** the v1 after-receipt existed; the fix was a pre-seat
   amendment adding the Q82 production-path counter, not a re-target. This is exactly the shape r34/r35 were
   rejected on, with two differences that keep it conforming: it happened before any wave seat scored (git log
   shows no seat receipts before `9c9bb64`), it is tightening-only with committed controls
   (`controls-q82.jsonl`), and the declaration pre-states the fallback if the closure disallows post-receipt
   rule additions — "the v1 rules stand alone and the receipts below are evidence that the v1 C1 counter is
   gameable (QUALITY 82), reported as a counter defect, not hidden" (SCORECARD.md:2137). Residual against B6:
   the cheapest mechanism-skip control was not built before freezing; the lane found it itself, which is good
   calibration but one step later than the bullet prescribes.
2. **r34 freeze breach (rules changed after seats scored) — NOT carried.** Amendment precedes all wave
   scoring; v1 counters never edited after freeze (B7 evidence).
3. **r36 frozen-counter-cannot-certify (probe S1 crash; after-value unreachable as declared) — mitigated,
   residual is environmental.** The new counters are small, self-tested, and sha-frozen; Q82 makes its
   environment demand (`unshare -rm`, bind over `/sys/fs/btrfs`) part of the claimed predicate via
   `ns_available == 1`. If the closure host denies user namespaces, C1 stops honestly under the declared kill
   rule rather than the counter silently failing — the r36 failure mode is claim-visible here.
4. **r37 sensitivity conjunct never delivered (no committed per-fix mutants reading > 0; kill evidence scored
   under the wrong probe version) — NOT carried.** Neither after-state contains a mutant/sensitivity conjunct;
   every kill rule is either fixture-receipted at freeze or a falsification condition with a named oracle (the
   pacman.log run-order seat; the HO1–HO7 per-row verdict seats; the S-row quote re-open).
5. **r37 counter amended after the change commit without a freeze sha — NOT carried** (B7: shas frozen in
   committed text; only counter-touching commit after freeze adds a new counter).
6. **r37 C3 moving snapshot (counts coupled to same-round commits) — NOT carried**: no calibration claim;
   measured revision declared before the after-run (SCORECARD.md:2124).
7. **Evidence-timing class (r34 future-dated READMEs; r35 heading-time recurrence; r36 bad stamp) — CHECKED,
   NOT carried in the declaration**: heading stamps equal committer dates to the minute (§0). Open exposure is
   elsewhere: the after/w1 receipts are untracked at this seat's run time and must be committed before filing
   (B7 watch item), and any wave-seat markdown that writes estimated UTC headings can still re-import the class.
8. **r34 unreceipted gate/claim lines — WATCH ITEM, not yet a defect**: the claim text is fully receipted; the
   receipts' committed status is pending (B7).

## 3. What I did not do

- I did not execute any counter, control script, selftest, gate or probe (sibling-owned instruments; read-only
  seat). All counter/control values above are re-typed from committed bytes at HEAD or from the named commits.
- I did not re-run the C2 per-row HO verdict seats' work (C2Rev*/C2Crit*/C2RevenConf items); their committed
  verdict files are a C2 kill-rule dependency, not part of this item.
- I did not verify the pacman.log run-order oracle seat's output (kill-rule instrument only; fires on
  contradiction).
- I did not check rounds 34–37 main lessons (`round-3*.md`), only the four verifier spot-checks the item names.
- No draft text is requested by this item, so none is proposed.
