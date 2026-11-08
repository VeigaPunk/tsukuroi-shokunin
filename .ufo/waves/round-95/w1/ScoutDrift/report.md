# ScoutDrift — planning data-walk and drift checks (round 95, wave w1)

Seat `ScoutDrift` (scout, axis `calibration`). Lane root
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (git branch `master`, jj-colocated; git HEAD detached —
**no mutating git/jj command was run**). Freeze commit `2abddda5`; wave-dispatch commit `884ed06b`;
tip observed during this seat `a302e688` (the L1's settle commit landed while the seat was running).

Receipts (this seat, written by me):
- `.ufo/waves/round-95/w1/ScoutDrift/claim-diff-claimsjson-vs-planfrozen.txt` — word-level diff of the four C1/C2 sentences in `claims.json` vs the plan's C1/C2 bodies and vs the plan's A1 block
- `.ufo/waves/round-95/w1/ScoutDrift/receipt-01-claim-texts.txt` — live-plan vs frozen-copy byte comparison
- `.ufo/waves/round-95/w1/ScoutDrift/receipt-03-manifest-verify.txt` — `sha256sum -c` on both manifests, the manifest's naming of the frozen copy, the per-commit re-pinning history
- `.ufo/waves/round-95/w1/ScoutDrift/receipt-04-registry-rows.txt` — the four rows and the `limine-pins` cells at the landed revision, the gate reading, the gate's own selftest
- `.ufo/waves/round-95/w1/ScoutDrift/receipt-05-ready-artifacts.txt` — the `.ready` artifacts, tracked vs untracked, per-round history for 84–95
- `.ufo/waves/round-95/w1/ScoutDrift/receipt-06-wave-shape.txt` — the 13 seats, their roles/axes, the attack share under two role sets, and the floor's text
- `.ufo/waves/round-95/w1/ScoutDrift/receipt-07-r94-routed-ledger.txt` — the r94 §6 routed items 1–10 with the artifact that closes each
- `.ufo/waves/round-95/w1/ScoutDrift/receipt-08-frontier-check.txt` — the three round-94 Frontier bullets verbatim, the r95 README addition, the "8"-readings classification, the `999999999.0.0` accepted row

Scratch: `/fast/scratch/hyaku/tsukuroi-r95/ScoutDrift` (deleted before this seat yielded; every number below
is reproducible from the commands quoted with it). Tooling: host `python3` 3.14.8 and `/usr/bin/git`
2.56.0; **no tool was installed or upgraded** (pacman is paused host-wide; nothing was needed).

---

## 1. The two frozen claim texts — `claims.json` vs `before/plan-frozen.md` vs the live plan

### 1.0 The three files are not three texts

```sh
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
diff .ufo/waves/round-95/before/plan-frozen.md .ufo/plans/round-95.md   # at 884ed06b: DIFF_EXIT=0
sha256sum .ufo/plans/round-95.md .ufo/waves/round-95/before/plan-frozen.md
# 41b15c4e762503aa1482fcb1cf1dacacdcb9a02eb9f090b0a48c8756e1502454  (both, at 884ed06b)
```

`before/plan-frozen.md` is a **mirror of the live plan, re-pinned in lockstep** at every freeze commit:

| commit | live plan sha256 | `before/plan-frozen.md` sha256 |
|---|---|---|
| `2abddda5` (freeze) | `6d060775…` | `6d060775…` |
| `a2ed6eee` (A1) | `46e6f268…` | `46e6f268…` |
| `884ed06b` (A2) | `41b15c4e…` | `41b15c4e…` |

So "the frozen copy" is not an independent pre-amendment snapshot; it verifies **by construction**, not by
freeze. (The r94 defect itself — a manifest that names the *live* plan and therefore `FAILED` at the tip —
is structurally closed: the manifest names the copy, and the live plan has since moved on without breaking
the manifest. See §2.) Receipt: `receipt-03-manifest-verify.txt`.

**Divergence 1 (live plan vs frozen copy, at the time of this seat).** The live plan now carries two
**post-scoring** amendments that the frozen copy does not:

```sh
sha256sum .ufo/plans/round-95.md .ufo/waves/round-95/before/plan-frozen.md
# 88137e047fe7a3030161f99563cc25a54392a2f8229ddfe212c0267159fd8207  .ufo/plans/round-95.md      (working tree)
# 41b15c4e762503aa1482fcb1cf1dacacdcb9a02eb9f090b0a48c8756e1502454  .ufo/waves/round-95/before/plan-frozen.md
```

- **A3 (post-scoring narrowing, citing `w1/ReviewBattery.md` F1)** — falsifies C1's predicate superlative
  "the largest in-bound member of the gate's published 1-9-digit component cap" (the cap is per component;
  `999999999.999999999.999999999` is in-bound and accepted) and narrows the claim to "a boundary member … the
  first component is 999,999,999, with the second and third components at 9". It states: *"`claims.json` is
  left byte-frozen (it is pinned in `before/instruments.sha256`); this amendment supersedes the predicate's
  superlative and is the ledger's `narrowing` pointer."*
- **A4 (post-scoring scope correction, citing wave artifacts)** — narrows C2's predicate (the registry gate's
  `PASS` certifies row **presence**, not the two `limine-pins` content cells), and re-binds C2's void clause
  to the sha256 of `tools/check-registry-coverage.py` because the freeze manifest pins no such entry.

Both A3 and A4 were in the live plan's working tree **uncommitted** while this seat measured
(`git diff .ufo/plans/round-95.md` → 36 insertions; `git log -1 -- .ufo/plans/round-95.md` → `884ed06b`).

### 1.1 `claims.json` vs the plan's own C1/C2 sentences

Word-level diff of each of the four fields per claim (`claim-diff-claimsjson-vs-planfrozen.txt`):

| field | claims.json vs plan-frozen.md | reading |
|---|---|---|
| C1 `predicate` | similarity 0.9805 — differs only in `9DIGIT:` vs `9DIGIT :` and a trailing period | **same sentence** |
| C1 `target` | similarity 0.3575 — the plan's C1 row body still carries the **pre-A1** text ("N05 … 0 error rows", "the r94 do-nothing battery on the landed gate: `unmet` `98/99`") | **A1 supersedes it** (A1's own words: "The live sentences are these (and `claims.json`), superseding the two sentences in the C1 row above") |
| C1 `kill` | similarity 0.6867 — same reason | **A1 supersedes it** |
| C2 `predicate` | similarity 0.9554 — claims.json says `status PASS`; the plan's C2 row body says ``status` `clean`` | **A2 supersedes it** (A2: "The predicate, target and kill rule now say `PASS`") |
| C2 `target` | similarity 0.8214 — `PASS` vs `clean` | **A2** |
| C2 `kill` | similarity 0.8936 — `PASS` vs `clean` | **A2** |

Against the plan's **A1 block** (the live sentences A1 quotes), `claims.json` C1 `target`/`kill` are
semantically the same sentences with three cosmetic differences plus one content difference:

- `['REFUSAL-VERSIONS-9DIGIT']` (claims.json) vs `["REFUSAL-VERSIONS-9DIGIT"]` (A1 block);
- `x3` vs `×3`; trailing `.` / capital `Unmet` vs `unmet`;
- **content:** claims.json's C1 `target` ends `… 0 REFUSAL-VERSIONS-9DIGIT rows in case_log (the family
  does not exist there)`, while the A1 block ends `… 0 REFUSAL-VERSIONS-9DIGIT rows in case_log.` — the
  parenthetical is in `claims.json` but **not** in A1's quoted sentence. It is a descriptive gloss carried
  over from the plan's own pre-A1 body sentence, and it does not widen the target.

**No unrecorded drift between `claims.json` and the plan's frozen copy.** Every divergence is A1, A2, A3 or
A4 — recorded amendments, named, not drift.

### 1.2 FINDING (calibration) — the frozen claim text still carries a superlative the wave falsified

`claims.json` is byte-frozen because it is one of the nine entries pinned in
`.ufo/waves/round-95/before/instruments.sha256` (`e9795dfc…`), and C1's kill rule says the claim is **void if
any instrument byte differs from that manifest at scoring time**. So `claims.json` cannot be corrected
without voiding C1 — which is exactly why A3 was written as a plan-only narrowing.

The consequence, measured: `claims.json` C1 `predicate` still says

> "the version `999999999.9.9` (the **largest in-bound member** of the gate's published 1-9-digit component
> cap, first component 999,999,999)"

and `w1/ReviewBattery.md` F1 (cited by A3) **falsifies that superlative**: the cap is per component, so
`999999999.999999999.999999999` is in-bound and the landed gate accepts it. The validator renders
`claims.json`; the narrowing that survives lives only in the (at the time of measurement) uncommitted live
plan. **A3 and A4 are also currently uncommitted** — `git log -1 -- .ufo/plans/round-95.md` is `884ed06b`
while the working tree carries A3+A4. If the L1 lands the plan without committing A3/A4, the recorded
narrowing is lost; if the L1 commits them, the frozen `claims.json` still says "largest in-bound member" and
the report's own C1 section must carry the narrowing for a reader. Two viable repairs, both the L1's call:
(a) land A3/A4 and have the report/ledger carry the narrowing pointer explicitly (A3's design), or
(b) re-pin `claims.json` + the manifest in a new freeze commit so the frozen sentence matches the
instrument, accepting that C1's kill rule is re-bound by that commit. [INFERENCE — I did not run the reviewer's
`boundary-probe.txt`; I read the falsification as quoted in A3 and the r95 README/knowledge entry, and
independently confirmed the gate's own bound is per component at
`tools/check-limine-pins.py:99` (`len(p) <= 9 for p in parts`) and that the corpus itself now records
`999999999.999999999.999999999` as in-bound and accepted.]

### 1.3 FINDING (calibration) — the plan's C2 row body is stale against its own amendment A2

`before/plan-frozen.md` lines 74, 80, 84 still read `status` `clean` in the C2 predicate, target and kill
rule, while `claims.json` reads `PASS` for all three. A2 (in the plan's amendments slot) says "The
predicate, target and kill rule now say `PASS`", and A2's evidence is the L1's own two receipts
(`after/c2-before-c0a20cef.json` reads `status FAIL`, `after/c2-after-b66e6be5.json` reads `status PASS`).
The live scoreboard is `PASS` — measured by me at `884ed06b`:

```sh
python3 tools/check-registry-coverage.py --revision 884ed06bdc7681ad73e757cf8a02bee21de2c480
# {"branch":"master","branch_tip":"a302e688…","counts":{"findings":0,"missing":0,"registered":151,
#  "rows_total":151,"tools_total":151},"findings":[],"revision":"884ed06b…","status":"PASS"}
python3 tools/check-registry-coverage.py --selftest
# PASS (23 cases, 23 passed, 0 failed)
```

The claim is not falsified (A2 recorded, evidence committed). But a reader re-deriving C2 from the plan's C2
row body — the way the r94 spot-check §6 item 3 warned — would look for a `clean` token the gate never emits.
`w1/CriticClaims.md` already records this as its finding (c). The cheap repair is an appended note in the
C2 row body saying "the live sentences are `claims.json`'s (A2)", not a rewrite of the frozen copy.

---

## 2. The freeze manifest at the current tree (item 3 of my brief)

```sh
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
sha256sum -c .ufo/waves/round-95/before/instruments.sha256
```

```
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r95.py: OK
tools/make-r95-bends.py: OK
.ufo/waves/round-95/before/controls/bends/N05-strict-8.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/waves/round-95/before/controls/do-nothing-battery-r94.py: OK
.ufo/waves/round-95/before/controls/do-nothing-gate-r94.py: OK
.ufo/waves/round-95/claims.json: OK
.ufo/waves/round-95/before/plan-frozen.md: OK
EXIT=0
```

- **PASS** — all 9 pinned entries verify, exit 0, at the current tree.
- `sha256sum -c .ufo/waves/round-95/before/freeze-manifest.sha256` → the same 9 lines, **exit 0**; the two
  manifests are **byte-identical** (`diff` → identical). r94's manifest had 11 entries including the live
  `.ufo/plans/round-94.md`; r95's has 9 and names the copy.
- **The r94 defect is closed as stated**: the manifest does **not** name the live plan.
  `grep -c 'plans/round-95.md' before/instruments.sha256` → **0**; `grep -c 'plan-frozen'` → **1**. The live
  plan has since moved (A3/A4, §1.0) and the manifest still verifies — exactly the failure mode that broke
  r94 (manifest `FAILED` at the tip) does not recur.
- **Residual, named**: because the "frozen" copy is re-pinned in lockstep with the live plan at each
  amendment commit (§1.0), the manifest verifies *by construction* rather than by freeze. The two entries
  that carry the round's meaning (`claims.json`, `before/plan-frozen.md`) were re-pinned twice after the
  initial freeze (`a2ed6eee`, `884ed06b` — receipt shows the two changed lines each time). The seven
  instrument entries (gate, battery, bend emitter, three controls) were pinned once at `2abddda5` and never
  moved; those are the ones the kill rules actually protect.
- **Finding (already in A4, independently confirmed here):** `tools/check-registry-coverage.py` is **not**
  pinned anywhere in the round-95 manifests (`grep -c 'check-registry-coverage' before/instruments.sha256`
  → **0**), and neither is `SKILL.md`. C2's kill clause "void if the registry gate bytes differ from the
  freeze manifest at scoring time" therefore has no referent. A4's repair (bind the gate's recorded sha256,
  `6fcb2d0a5f1b2493aa505e179aa013b479e2a06894152d3b206e017720a24812` at this tree) is the right shape; I
  recorded the digest in `receipt-04-registry-rows.txt`. **The same hole exists on the r94 manifest** (its
  11 entries do not name the registry gate either), so this is an inherited hole, not a new one.

---

## 3. The r94 spot-check §6 routed items 1–10, with the artifact that closes each

Queue source: `corpus/lessons/round-94-verifier-spotcheck.md` §6. Evidence: `receipt-07-r94-routed-ledger.txt`.

| # | r94 routed item | state | artifact that closes it / why it stays open |
|---|---|---|---|
| 1 | Gate registry: add rows for the r94 and r95 tools; `limine-pins` row must read default `auto` and 39 fixtures | **closed** | `SKILL.md:5934–5937` at `a302e688` carry the four rows; the `limine-pins` row reads ``default `auto` `` and `39 fixtures` (grep at the landed revision). The gate reads `PASS`, findings 0, missing 0, tools_total 151, registered 151, `--selftest` PASS 23/23. **Caveat (A4, ExecRegistry, ReviewRegistry):** the gate certifies row **presence**, not content — three cells of the four new rows are false as written (ReviewRegistry), and they sit outside C2's two certified cells, so C2 is unaffected; the cells are routed, not scored. |
| 2 | `.ready` bookkeeping: commit the dispatch artifact; give `WAVE-DONE` an artifact | **half closed — open on the dispatched file** | `.ufo/waves/round-95/w1.ready` **exists and is tracked/committed at the tip** (in `git ls-tree a302e688`). But `.ufo/waves/round-95/w1.ready.dispatched` is **untracked** (`git status --porcelain` → `?? .ufo/waves/round-95/w1.ready.dispatched`; `git log --all -- …w1.ready.dispatched` → empty). Rounds 84–93 each track **both**; r94 tracked neither; r95 tracks one. The plan's disposition 2 promised "the r95 wave commits `w1.ready` and `w1.ready.dispatched`" — the second file is still uncommitted. **One `git add` at settle closes it.** |
| 3 | Freeze manifest vs the plan: pin a frozen copy under `before/` (or drop the plan from the manifest) | **closed (r94's failure mode)** | manifest names `before/plan-frozen.md`, not the live plan; `sha256sum -c` exit 0 on both manifests (§2). Residual named in §2: the copy mirrors the live plan instead of freezing it. |
| 4 | Do-nothing arithmetic and the stderr clause: the r93 gate reads `97/98`, not `96/98`; a stderr-only fake is refused | **closed** | r95 report line 78: "the r93 gate reads `97/98 unmet` on the r94 roster and refuses a stderr-only fake like the V4 probe (`p.stdout` only)"; r95 lesson line 210 the same. Independently confirmed the clause's mechanism: `before/controls/do-nothing-gate-r93.py:117` searches `p.stdout` only. |
| 5 | Report prose counts: every count copied from a named artifact and re-counted before filing | **closed by the report's own discipline** | r95 report line 79: "every count here is copied from a named artifact and re-counted before filing". Re-checking the report's counts against artifacts is the closure's job, not this seat's. |
| 6 | Uncited final commit `029f6629` → name it | **closed** | named at r95 report line 238 (full hash) and line 80; the r94 report is **not** rewritten (`grep -c 029f6629 .ufo/reports/round-94/tsukuroi.md` → 0). |
| 7 | r93 routed-item mapping: map the queue **by its own text**; carry what did not close | **open on one half — unsourced label** | The r95 plan's disposition 7 and the r95 lesson both say "routed 4's M12 timeout survivor and routed 5's `VERDICT-INCOMPLETE` stay open and are named, not closed". **r93's own routed 5 is "Probe grammar leniency (suffix / extra components)"** (`corpus/lessons/round-93-verifier-spotcheck.md:110`), and the token `VERDICT-INCOMPLETE` appears in **no** spot-check §6 in `corpus/lessons/` — its only occurrence in the whole lessons corpus is the new `round-95.md` itself. So the r95 mapping names, by a token with no antecedent, an item it claims to map "by its own text" — the exact defect class r94 §6 item 7 routed. The **M12 half is right** (r93 routed 4 does name the M12 timeout error-row shape). The substance of r93's routed 5 *is* carried, but under a different number: the r95 lesson maps r94 routed 9's first half — the `12.9.6.1` extra-component shape — to the Frontier (lesson:211, README:1147), which is the same ground as r93 routed 5's "extra components". **Repair (one sentence):** rewrite the carried item as "r93 routed 5 (probe grammar leniency — suffix / extra components), whose extra-component half stays on the Frontier per r94 routed 9" and drop the unsourced `VERDICT-INCOMPLETE` token, or cite the queue item it comes from. |
| 8 | Battery docstring vs its own fixture: `fam_auto_probe_shapes` claims the stderr shape "belongs to the gate's selftest, not this family" while the fixture emits it; `REFUSAL_DIGIT9` declared and referenced nowhere | **half closed — the stderr half is still open, and the report's claim about it is wrong** | `REFUSAL_DIGIT9` half **closed**: the r95 battery references it at `tools/limine-pin-battery-r95.py:1715` (`_era_first_line_panic(c, REFUSAL_DIGIT9)`), so the declared-and-unused defect is gone. **stderr half still open**: the r95 battery's `fam_auto_probe_shapes` docstring is **byte-identical** to r94's and still carries "The stderr shape belongs to the gate's selftest, not this family" (r95 battery `:1726`), while the fixture *does* emit stderr (`AUTO_PROBE_SHAPES` at `:1718` includes `stderr:12.9.6`; `:1935–1937` say the fake prints "a version on stderr"). The r95 report line 84 says "stderr sentence is left as r94 wrote it and **the correction is recorded in the lesson**" — but the correction is **not in the lesson**: `grep -c AUTO-PROBE-SHAPES corpus/lessons/round-95.md` → **0**, and the lesson's three `stderr` hits are the S389 4300-digit quote, the error-row text, and routed item 4's `p.stdout` clause — none corrects the family docstring. **The lesson must carry the correction or the report's sentence about it must be withdrawn.** |
| 9 | Coverage gaps: the `12.9.6.1` extra-component shape is not exercised at battery level; an over-strict `<= 8` gate scores `met` 98/98 | **closed as routed (second half), first half on the Frontier** | The `<= 8` over-strict gate is now killed by the frozen one-clause bend `N05-strict-8` (reads `unmet` with `REFUSAL-VERSIONS-9DIGIT`; A1 records the four error rows as the bend's refusal receipt). The `12.9.6.1` extra-component shape stays explicitly on the Frontier (README:1147, lesson:211). |
| 10 | Contested scope: kaidoku/revenger reverse-engineering ownership is unruled | **carried, reported, not absorbed** | r95 lesson:185 and :212 name it (`R20-OUT009`, tsukuroi `ADJ-06`) as operator-owned; `w1/ConnectorOverlap.md` found no sibling claiming it. |

---

## 4. Frontier check — the three round-94 Frontier bullets vs the r95 work

Bullets verbatim: `corpus/README.md:1108–1117` (receipt `receipt-08-frontier-check.txt`).

**Bullet 1** — the ten-digit enumeration and the probe-shape family "are the r93 survivors' closures; each is
killed by a one-clause bend (N01/N03, N02) at `unmet` with the family in `failed_families` and 0 error rows."
→ **not contradicted.** The r95 battery keeps both families byte-identical (docstring byte-compare: identical)
and adds a third; the frozen bend set for r95 is N05 only, so N01/N03/N02 were **not re-run under the 99-family
roster** — the bullet's "0 error rows" property for those bends survives as a r94-roster reading and is simply
not re-certified at the new roster. (Consistency note: under bend N01 (`<= 10`) the new family still passes —
`999999999.9.9` is 9 digits — so the 9-digit family does not become an error-row source there.)

**Bullet 2** — "the r92 launcher residuals stay open; the r93 AUTO-fake literal leakage is disclosed in the
battery docstring (CriticForgers f6), not closed."
→ **not contradicted.** The leakage-disclosure paragraph is **byte-identical** in the r95 battery
(`LEAKAGE-PARAGRAPH IDENTICAL: True`), so the disclosure persists and the item stays open exactly as the
bullet says. The r95 README's new bullets keep the r92 residuals on the Frontier (README:1147).

**Bullet 3** — "The `auto` default is now the gate's default … and `999999999.0.0` (accepted) certifies the
9-digit cap from inside."
→ **not contradicted, but now qualified.** The accepted row survives byte-for-byte: the r95 battery's
`--usage-check` roster is **byte-identical** to r94's and still carries `("999999999.0.0", 0)`. What the r95
work adds is the *scope* of that certification: the cap is **per component**, so the accepted leg is
"**X-certified only**" (r95 README bullet 1; `knowledge/limine-bound-9digit-r95.md` Limits). `999999999.0.0`
has its first component at the cap and its second and third at 1 digit, so it certifies the X position only —
which is exactly the qualifier the same knowledge entry and A3 record. `corpus/README.md` is append-only, so
the r94 bullet and the r95 qualifier must be read together; the r94 bullet's "certifies the 9-digit cap" is
now true only in the X position. This is the same fact that falsified C1's predicate superlative (§1.2).

**On the "accepted boundary is raw 8" readings.** No corpus text claims the accepted boundary is 8. I
classified every "8" reading that could be mistaken for one:
- `raw 8-9` in `corpus/SOURCES.md:394` (S383) and `corpus/knowledge/limine-version-probe-r93.md:21,65` — this
  is the **raw.githubusercontent line range 8–9** of the Limine ChangeLog, i.e. a *source locator*, not a digit count;
- `<= 8` in the r94 spot-check §6 item 9 — the **over-strict mutant** whose blindness r95 closes;
- `<= 8` in r95's N05 bend / mutant M01 / the "X-certified only" Frontier bullet — a **mutant bound**, never a
  claim about the published cap;
- `1-8`-style prose — none.
So no reading anywhere asserts an accepted boundary of 8 digits, and the r95 work does not create one.

---

## 5. The wave's shape and attack share (item 5 of my brief)

From `.ufo/waves/round-95/w1-spec.json` (13 items, `maxLanes` 16, `reportDir .ufo/waves/round-95/w1`):

| seat | role | axes |
|---|---|---|
| ExecBattery | executor | depth |
| ExecBend | executor | depth |
| ExecDoNothing | executor | depth |
| ExecRegistry | executor | operability |
| ScoutSources | scout | freshness |
| **ScoutDrift** | scout | **calibration** |
| ScribeKnowledge | scribe | depth |
| ScribeLesson | scribe | calibration |
| ReviewBattery | reviewer | depth |
| ReviewRegistry | reviewer | operability |
| CriticClaims | critic | depth, operability |
| MutBound | mutation-tester | depth |
| ConnectorOverlap | connector | adjacency |

**The 25 % floor** (fleet addendum, `scripts/hyaku/lane-addendum.md`, run-15 binding):
"ONE v1 wave of 8–16 seats under `ufo-wave-policy.json` (band 8–16), **≥25 % attack seats (reviewer, critic,
mutation-tester, labrat)**, at most 2 connector seats; residual ≤4 seats in one ordinary task call, counted in
the round total. 8 is the protocol L2 floor."

**The wave's attack share:**
- by the floor's own role list (reviewer, critic, mutation-tester, labrat): 2 reviewers + 1 critic +
  1 mutation-tester = **4/13 = 30.8 %** → **meets the ≥25 % floor** (margin 5.8 points, i.e. 3.25 seats' worth
  of slack is not needed: 3 seats would have been 23.1 %, so the wave's fourth attack seat is what clears the floor);
- by the falsification ledger's role set (`scripts/hyaku/prefile-falsification.py:58` `ATTACK_ROLES` =
  reviewer, security-reviewer, critic, mutation-tester, sentinel, connector, revenger, labrat — the connector
  counts): **5/13 = 38.5 %** → also meets it.
- The plan's own §"Round shape" text says "2 reviewer + 1 critic + 1 mutation-tester = 4/13 = 31 % (≥25 %)" — that
  matches the spec exactly (the plan rounds 30.8 % to 31 %).
- Other floor clauses: band 8–16 → 13 seats ✔; L2 floor 8 ✔; at most 2 connector seats → 1 ✔; residual ≤4 seats
  in one ordinary task call → the plan declares "Residual call: none" ✔.

**Minor finding (calibration, low severity):** `w1-spec.json`'s top-level `axes` list is
`['depth','operability','freshness','calibration']` while the `ConnectorOverlap` item carries
`axes: ['adjacency']` — an axis that is not in the spec's own list. The plan's Round shape says the adjacency
item is "reported, not absorbed" (kaidoku/revenger RE ownership is operator-owned), so the seat is
defensive rather than absorbed; the mismatch is in the spec's `axes` field, not in the work.

---

## 6. Summary of findings (calibration axis)

| # | finding | severity | evidence |
|---|---|---|---|
| F1 | The frozen `claims.json` C1 predicate still asserts "the largest in-bound member" — falsified by `w1/ReviewBattery.md` F1 (the cap is per component). The narrowing exists only as plan amendment A3, and at the time of this seat A3/A4 were **uncommitted** in the working tree. `claims.json` cannot be edited without re-pinning the manifest (C1's void rule). | **high** (claim wording vs instrument) | `receipt-01`, §1.0–1.2; `sha256sum .ufo/plans/round-95.md` vs `before/plan-frozen.md` |
| F2 | The r95 plan/lesson name r93 routed 5 as `VERDICT-INCOMPLETE`; r93's own routed 5 is "Probe grammar leniency", and that token appears in no spot-check §6 in the corpus. The r94 lesson carried the same class of mis-mapping. | medium (queue-by-own-text) | `receipt-07` §routed 7; `corpus/lessons/round-93-verifier-spotcheck.md:110`; `grep -rl VERDICT-INCOMPLETE corpus/lessons/` |
| F3 | The r95 report says the `fam_auto_probe_shapes` stderr correction "is recorded in the lesson"; it is not in the lesson (`grep -c AUTO-PROBE-SHAPES corpus/lessons/round-95.md` → 0), and the wrong sentence is still byte-identical in the r95 battery at `:1726`. | medium (r94 routed 8, second half) | `receipt-07` §routed 8 |
| F4 | `w1.ready.dispatched` is still untracked at the tip while rounds 84–93 track both `.ready` files; the plan's own disposition 2 promised both committed. | low (one `git add`) | `receipt-05` |
| F5 | The plan's C2 row body still reads `status` `clean` (3 places) against A2's `PASS`; a reader re-deriving from the row body looks for a token the gate never emits. | low (readability) | `receipt-01`, §1.3; `w1/CriticClaims.md` finding (c) |
| F6 | `before/plan-frozen.md` mirrors the live plan and is re-pinned at each amendment, so the manifest verifies by construction rather than by freeze; and the registry gate / `SKILL.md` are pinned nowhere, leaving C2's original void clause without a referent (A4 re-binds it; the same hole is inherited from r94). | low-medium (structural) | `receipt-03` |
| F7 | `w1-spec.json`'s top-level `axes` omits `adjacency` although the ConnectorOverlap item carries it. | low | `receipt-06` |

**No unrecorded drift** was found between `claims.json` and the plan's frozen copy: every divergence is a
recorded amendment (A1, A2 in the frozen copy; A3, A4 in the live plan). Every number quoted above was
produced by a command in this report, and the corresponding raw output is in this seat's receipts.

Tool installs: none. No pacman transaction. No mutating git/jj command, no write outside
`.ufo/waves/round-95/w1/ScoutDrift/` and the seat report file, no instrument edited, no scratch left behind.

{"seat":"ScoutDrift","verdict":"findings","notes":"Planning data-walk + drift checks. claims.json vs before/plan-frozen.md: every divergence is a recorded amendment (A1/A2 in the frozen copy; A3/A4 in the live plan), no unrecorded drift. FINDINGS: (F1, high) frozen claims.json C1 predicate still says 'the largest in-bound member', falsified by ReviewBattery F1 (the cap is per component; 999999999.999999999.999999999 is in-bound and accepted); claims.json is manifest-pinned so C1's kill rule bars editing it, the narrowing lives only in plan amendment A3 - and A3/A4 were still UNCOMMITTED in the working tree at measurement time (git log -1 on .ufo/plans/round-95.md = 884ed06b, working tree sha 88137e04). (F2) r95 plan/lesson name r93 routed 5 as VERDICT-INCOMPLETE, but r93's own routed 5 is 'Probe grammar leniency' and that token appears in no spot-check section 6 in corpus/lessons - the r94 lesson carried the same mis-mapping class. (F3) the r95 report says the fam_auto_probe_shapes stderr correction is recorded in the lesson; it is not (grep -c AUTO-PROBE-SHAPES corpus/lessons/round-95.md = 0) and the wrong sentence is still byte-identical in the r95 battery at :1726. (F4) w1.ready.dispatched is untracked at the tip while rounds 84-93 track both .ready files. (F5) the plan's C2 row body still reads 'status clean' against A2's PASS. (F6) before/plan-frozen.md mirrors the live plan and is re-pinned per amendment (verifies by construction, not by freeze); the registry gate and SKILL.md are pinned nowhere, so C2's original void clause had no referent (A4 re-binds it; inherited from r94). (F7) w1-spec axes omits adjacency although ConnectorOverlap carries it. OTHER MEASUREMENTS: sha256sum -c before/instruments.sha256 = 9/9 OK exit 0 at the current tree; freeze-manifest.sha256 identical to instruments.sha256 and also exit 0; the manifest names 0 live-plan entries and 1 frozen-copy entry, so the r94 defect (manifest FAILED at tip) is structurally closed. r94 routed 1-10 ledger: 1 closed, 2 HALF (dispatched file untracked), 3 closed, 4 closed, 5 closed by the report's discipline, 6 closed (029f6629 named at r95 report :238/:80, r94 report not rewritten), 7 OPEN (F2), 8 HALF (F3), 9 closed with the 12.9.6.1 shape on the Frontier, 10 carried/operator-owned. Frontier: none of the three round-94 bullets is contradicted - the leakage-disclosure paragraph and the usage roster are byte-identical in the r95 battery, and the '999999999.0.0' accepted row survives byte-for-byte, now qualified as X-certified-only (the same fact that falsified F1); no corpus reading asserts an 8-digit accepted boundary ('raw 8-9' is the S383 ChangeLog raw line range; '<= 8' is a mutant bound). Wave shape: 13 seats, attack share 4/13 = 30.8% by the floor's own role list (reviewer, critic, mutation-tester, labrat) and 5/13 = 38.5% by the falsification ledger's role set (connector counts) - both meet the >=25% floor from scripts/hyaku/lane-addendum.md run-15; band 8-16 OK, 1 connector <= 2, L2 floor 8 OK. No tool installed or upgraded (pacman paused host-wide); python3 3.14.8 and git 2.56.0; scratch deleted; no mutating git/jj command; no instrument edited."}
