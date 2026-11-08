# Round 95 verifier spot-check — tsukuroi lane

author: hyaku closure (non-author integrator, @m_zfl)

Lane HEAD before the round: `c0a20cef641ada6feeab1ca107ea62c1848d1da0`; after: `b8f878c88fa795fbf20d6129807dfc5222e5fadf`
(cited in the closure brief and re-measured here). Driver digest (copied from the mutable
`.ufo/watchdog.log`): `2026-11-08T06:41:58-03:00 launch tsukuroi round=95 pgid=3745292
driver=hyaku-inline attempt=1`; `2026-11-08T07:21:10-03:00 complete tsukuroi round=95; hyaku-inline
attempt=1`.

## 1. Conformance (step 1)

- **Report landing and attribution**: fleet repo, `git log --format='%an %H' --
  .ufo/reports/round-95/tsukuroi.md` → `tsukuroi-shokunin <tsukuroi@shokunin.local>
  cf0a19cc368cd8346a3e1fbc4f8d45ca6ccf61d2 2026-11-08 07:20:30 -0300 round-95: tsukuroi report`.
  Committed by the lane identity (not swept), and on `origin/main`. The lane's last commit
  `b8f878c8` is 07:20:05, so the report lands after its commit. Pass.
- **`SHONEN` heading**: `grep -c '^## SHONEN' .ufo/reports/round-95/tsukuroi.md` → `1`, followed by
  four `[~]` lines (one per box, each with a resolvable pointer) and no self-attested `[x]`. Pass.
- **Cited lane commits**: `git -C tsukuroi-shokunin merge-base --is-ancestor <hash>
  refs/heads/master` → `2abddda5` OK, `a2ed6eee` OK, `b66e6be5` OK, `884ed06b` OK, `a302e688` OK,
  `0afeb7d9` OK, `b8f878c8` OK, plus the r94 final commit `029f6629` OK; `c0a20cef` is an ancestor
  of the tip. (The report's `d66b4a59…`/`7d79ac29…` are sha256 prefixes of tool bytes, not commits.)
  Pass.
- **Clean and pushed**: `scripts/hyaku/jj-lane.sh state tsukuroi-shokunin` → `branch=master
  local=b8f878c88fa795fbf20d6129807dfc5222e5fadf remote=b8f878c88fa795fbf20d6129807dfc5222e5fadf
  ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` → 0 lines;
  `git ls-remote origin refs/heads/master` → `b8f878c8…`. Pass.
- **Prompt fidelity**: `.ufo/prompts/tsukuroi-round-95.md` (140391 bytes) committed by
  `tsukuroi-shokunin 83fe13df` (06:41:56, two seconds before the launch line). A mechanical line
  check of `templates/round-prompt.md` against the prompt (substituting `{{LANE}}`/`{{ROUND}}`/
  `{{FLEET_ROOT}}`/`{{AXES}}`) finds 139 of 140 template lines verbatim; the one difference is the
  expected rendering substitution on line 1 (working dir printed literally). The hyaku §6 addendum
  carries the round-level contract: mission/axes binding (§1), the 1–3 claims rule and the lowest-axis
  duty (§2), the frontier step (§2b), the L2 floor "at least 8 L2 subagents in ONE batched
  AgentSwarm call" (§3), the report path and sections (§4), commit-then-push and push scope (§5), the
  L0 side channel (§5). The five child-lane items are present: report path/filename (§4 line 101),
  commit-before-report ordering (§5 "the report lands last and cites the pushed lane hash"), `SHONEN`
  heading (§4 + addendum item 4), commit-hash citation (§4 "tied to the commit hash that carries it"),
  lane write scope (addendum item 3). The prompt's binding run-15 route map is quoted; `MISSION.md`'s
  role-class table is explicitly advisory and pins no model, so no bucket mismatch is gradeable, and
  the prompt names `task.agentModelOverrides` as the routing authority. Pass.
- **Marker test**: real report — 274 lines, per-item evidence pointers, changes tied to `LOG.md`
  ("Round 95 — freeze/C2/wave/settle"), checkable commit citations, both trend sections. Status `ok`.
- **Wave shape**: `w1-spec.json` 13 items, `maxLanes 16` (run-15 band 8–16); roles executor ×4,
  scout ×2, scribe ×2, reviewer ×2, critic ×1, mutation-tester ×1, connector ×1 → 4/13 = 31 % attack
  (≥25 %), 0 dead; `w1-dispatch.json` `counts` 13 spawn / 0 resume / 13 total; `w1-validate.err`
  0 bytes; `w1.ready` and `w1.ready.dispatched` committed (the r94 routed-2 debt); 13 seat report
  files under `w1/`. The L1 holds the §3 planner seat per the prompt's explicit orchestrator ruling
  (line 394) and records the ScoutDrift data-walk; not a defect.
- **Fleet-repo leftovers**: `.ufo/l0-questions.md` carries two uncommitted *tsukuroi round-92* lines
  (the credential-incident line and its supersede pair), not round-95 work; `.scratch/…` is
  orchestrator-owned. Neither is lane round-95 debt; left untouched.

**Conformance defects found here (status-neutral; §6 routes them)**: the report's ledger paragraph
undercounts its own wording rows ("four" vs six committed); `corpus/QUALITY.md` is unchanged while
lesson M1 records `captured-by: none`; C2's void clause names a gate sha256 "recorded in the C2
receipt" that no receipt records; the report lists two revisions (`0afeb7d9`, `b8f878c8`) as
measured registry-PASS points with no per-revision receipt; two frozen tool docstrings still carry
the A3-falsified superlative; the README's A4 sentence over-scopes "the instrument".

## 2. Claims — re-derived by the closure

Commands run inside `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; receipts are re-parsed from
committed bytes at `b8f878c8`, and the two counting facts below are re-derived with my own parsers,
never copied from the report.

### C1 — depth 8 (tied lowest non-retired axis); accepted leg of a published bound — **met** (wording narrowed by A3)

| measurement (mine) | command | observed |
|---|---|---|
| roster size before / after | parse `FAMILY_ROSTER` in `tools/limine-pin-battery-r94.py` / `-r95.py` at `b8f878c8` | 98 unique / **99 unique**, `REFUSAL-VERSIONS-9DIGIT` ×1 |
| do-nothing control identity | `cmp` r94 battery vs `before/controls/do-nothing-battery-r94.py` | **IDENTICAL** |
| N05 one-clause delta | `diff -u tools/check-limine-pins.py before/controls/bends/N05-strict-8.py` | one line: `len(p) <= 9` → `len(p) <= 8` |
| freeze pin | `sha256sum -c before/instruments.sha256` and `-c before/freeze-manifest.sha256` from a `git archive b8f878c8` tree | **9 × OK** / all OK |

| receipt | runs | verdict | passed | failed_families | 9-digit rows (passed) | case errors |
|---|---|---|---|---|---|---|
| `after/c1-canonical.json` | 3 | `met` ×3 | 99/99 | `[]` | 4 (4) | 0 |
| `w1/ExecBattery/c1-clone.json` (clone at `884ed06b`) | 3 | `met` ×3 | 99/99 | `[]` | 4 (4) | 0 |
| `after/n05-canonical.json` | 3 | `unmet` ×3 | 98/99 | exactly `["REFUSAL-VERSIONS-9DIGIT"]` | 4 (0) | 4 (rc-64 refusal) |
| `w1/ExecBend/n05-clone.json` | 3 | `unmet` ×3 | 98/99 | exactly `["REFUSAL-VERSIONS-9DIGIT"]` | 4 (0) | 4 |
| `after/dn-n05-canonical.json` (r94 roster) | 3 | `met` ×3 | 98/98 | `[]` | 0 | 0 |
| `after/dn-gate-canonical.json` (r94 roster) | 3 | `met` ×3 | 98/98 | `[]` | 0 | 0 |

Mutation evidence: 8 one-clause mutants under `w1/MutBound/mutants/` (+ the emitter); the committed
`receipts/summary-table.txt` reads **7 KILLED / 1 SURVIVED**, with M01/M03/M07 killed by
`REFUSAL-VERSIONS-9DIGIT` alone and M06 (echo a wrong `limine_version` for an explicit version)
surviving — reported, not hidden. The A1 target's error accounting matches the receipts exactly
(0 error rows on the landed-gate legs; 4 on the bend leg, the bend's own rc-64 refusal). The A3
narrowing is required: the frozen predicate's "largest in-bound member" is false under the
per-component cap (`w1/ReviewBattery.md` F1), and the report/knowledge entry use the narrowed
"boundary member, first component at the cap". **Met.**

### C2 — operability 9 (assurance arm); the lane's registry gate — **met**

My own parser (independent of `tools/check-registry-coverage.py`) over the highest-numbered
`## Gate and probe registry — roundN superseding current rows` section of `SKILL.md`:

| revision | registry rows (my parse) | distinct `tools/` paths named | regular `tools/` blobs | missing | orphan |
|---|---|---|---|---|---|
| `c0a20cef` | 147 | 147 | 149 | `tools/limine-pin-battery-r94.py`, `tools/make-r94-bends.py` | none |
| `b8f878c8` | **151** | **151** | **151** | **none** | none |

Committed gate receipts: `after/c2-before-c0a20cef.json` → `status FAIL`, findings 2, missing 2,
tools 149, registered 147 (revision pinned to `c0a20cef`); `after/c2-after-b66e6be5.json`,
`w1/ExecRegistry/tip-registry.json` (`884ed06b`), `w1/CriticClaims/registry-tip-a302e688.json` →
`status PASS`, findings 0, missing 0, 151/151; an independent coverage receipt
(`w1/ReviewRegistry/receipts-10-independent-coverage.txt`) agrees 151/151 with no missing paths.
Selftests (committed): registry gate `PASS (23 cases, 23 passed, 0 failed)`; `limine-pins`
`selftest PASS 39/39` (39 PASS lines, 0 FAIL). The `limine-pins` row reads `default auto` and
`(39 fixtures`; the two r94 tools were absent from `SKILL.md` at `c0a20cef` (`grep` → no hit) and
the four r94/r95 rows exist at the tip. `SKILL.md` and `tools/` are byte-identical from `a302e688`
to `b8f878c8` (`git diff --stat` → 0 lines), so the tip value carries. **Met.**

### 2b Pre-file falsification ledger (addendum §8, Amendment 59)

`python3 scripts/hyaku/prefile-falsification.py --lane tsukuroi --round 95` →

```
PREFILE-FALSIFICATION: pass claims=2 rows=21 attack_seats=5 findings=0
```

exit **0**. The committed artifact is `tsukuroi-shokunin/.ufo/waves/round-95/claim-falsification.tsv`:
21 rows, both claims covered (C1 ×14, C2 ×7), all five attack seats present (ReviewBattery,
ReviewRegistry, CriticClaims, MutBound, ConnectorOverlap), 14 neutral + **6** `falsifies-wording` +
**1** `falsifies-number`. Adjudication: the wording rows point at A2 (plan body still said `clean`),
A3 (the "largest in-bound member" superlative; two rows) and A4 (the roster-vs-instrument blindness,
three rows) and each names its narrowing — real and reconciled, so C1/C2 verify with the narrowed
sentences. The number row (A1: pre-freeze "0 error rows" and "unmet 98/99") names the amendment and
voids no receipt. The report's own sentence says "four `falsifies-wording` rows": that count is wrong
(§6 item 1) but the ledger itself is sound.

### 2c Gate standard (Closure consequence)

I did not execute either lane gate. Committed evidence verified: the self-test tallies above, the
frozen run verdicts naming the revision measured (`884ed06b` for the C1 legitimate run and its clone,
`b66e6be5`/`884ed06b`/`a302e688` for C2), and the freeze manifests re-checked from a `git archive` of
the tip. Gate bytes are unchanged this round (`tools/check-limine-pins.py` sha256 `7d79ac29…`,
registry gate `6fcb2d0a…`; `git diff --stat c0a20cef b8f878c8 -- tools/check-*.py` empty). Defect:
C2's void clause (A2-corrected) binds "the sha256 of `tools/check-registry-coverage.py` recorded in
the C2 receipt"; no round-95 receipt records it — I measured `6fcb2d0a5f1b…` at the tip instead
(§6 item 3).

## 3. Discernment spot-check (`corpus/lessons/round-95.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S389 — Python 3 docs, integer string conversion length limitation (new row) | admit | `https://docs.python.org/3.15/library/stdtypes.html#integer-string-conversion-length-limitation`, fetched 2026-11-08 by the closure: **815447 bytes, sha256 `6bf2ce2b…`**, the `4300` sentence at byte **785297** verbatim, the `ValueError` sentence at byte **782228** | **agree** | the quote is verbatim at the stated offset and the pin reproduces exactly; the page is upstream's statement of the CPython limit, and the entry explicitly does not claim Limine behaviour from it |
| `https://man.archlinux.org/man/limine.8` | reject | fetched 2026-11-08: **HTTP 404, 2706 bytes**, body "Page not found" | **agree** | no such page exists; nothing to admit, and the r94 rejection was for the same reason |
| `https://api.github.com/repos/Limine-Bootloader/Limine/releases/tags/v12.9.6` | reject | fetched 2026-11-08: HTTP 200, **22555 bytes** today (the seat recorded 26652 — a mutable API payload), body points at the ChangeLog and carries tarball-signature text | **agree** | the body states no Limine behaviour; the byte-count drift is the payload's mutable fields, not a conflict with the refusal |
| S389 row in `corpus/SOURCES.md` — `teaches` quote | new-row quote check | same page fetch; quoted sentence "The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits." (14 words) | **agree** | ≤25 words, verbatim, and the row's anchor (section id, byte 780197/785297) resolves |

**Census**: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` →
exit **0**, `tsukuroi ok …/corpus/SOURCES.md`, 57 W04 + 1 W01, **0 E** findings; rows
`git show c0a20cef:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'` → 388 and the tip →
**389**; `git diff --numstat c0a20cef b8f878c8 -- corpus/SOURCES.md` → `1 0` (S389 added, no cell
edited in place).

## 4. Axis verdicts (diff `c0a20cef…b8f878c8`)

| axis | verdict | evidence |
|---|---|---|
| depth | **improved** | C1 verified: 98 → 99 families, the accepted leg of the published bound now certified (99/99 met ×3 canonical + clone; N05 98/99 ×3 both layouts with the family named); 7/8 mutants die. The lane's ordinal score stays 8 (no uplift, stated) — the axis moved by evidence. |
| operability | **improved** | C2 verified: registry gate `FAIL` (2 findings, 149/147) → `PASS` (0, 151/151) at the landed tip, both selftests green; the `limine-pins` cells repaired. Score stays 9 (assurance repair, stated). |
| coverage | unchanged | no `PROVINCE.md` change and no new surface claimed; the README round-95 section is ground, not surface. |
| freshness | unchanged | no claim; S386/S387/S388 re-opened byte-identically (frontier step, not an axis move). |
| calibration | unchanged | the lane's self-assessment (axes 8/9/9/9/9/8, both claims "met") matches my measurements, and the A1/A3/A4 narrowings are recorded rather than papered over — but no calibration claim landed. |
| adjacency | unchanged | connector: no sibling duplicate or contradiction across 20 sibling repos; the kaidoku/revenger ownership stays unruled, reported and not absorbed. |

**No axis harmed**: both gates byte-unchanged; the r94 roster still reads `98/98 met` on the landed
gate ×3; `corpus/` is additive (one entry, one row, `1 0` numstat); no capability, row or file was
removed; `SKILL.md`'s only change is the registry repair.

## 5. Trends

- **expansion — improved.** SOURCES 388 → 389 (my count, census exit 0) and one admitted knowledge
  entry on ground the coverage map did not hold (`knowledge/limine-bound-9digit-r95.md`, the accepted
  leg; README "Round 95 — the accepted leg…"), citing the `mined` S389 row whose `used-by` paths
  exist (E11 clean).
- **quality — improved.** The entry deepens the held bound rule (QUALITY 139's accepted leg is now
  executed by a family, not only by a usage row); S386/S387/S388 were re-opened byte-identically, so
  the r94 entries' sources re-verified; the lane's registry inventory went from red to green; no
  admitted entry fails its re-check (I sampled the new entry and the S389 row). Defect: no
  `QUALITY.md` criterion was added for lesson M1 despite `captured-by: none` (§6 item 2).
- **discernment — improved.** Three wave artifacts forced three honest narrowings (A2/A3/A4), each
  named in the ledger with its amendment; M06's survival is reported; my outside spot-check agrees
  on the sampled admit (S389) and both rejects (404 man page; API release page) with no disagreement
  left unlearned.

## 6. Routed defects (the lane fixes these next round)

1. **Report prose count (r94 routed-1 recurrence).** The ledger paragraph says "the four
   `falsifies-wording` rows"; the committed `claim-falsification.tsv` has **6** (`F1` class plus
   A2/A3/A4), 1 `falsifies-number`, 14 neutral of 21. Correct in the next report or an erratum —
   never rewrite the filed bytes.
2. **`corpus/QUALITY.md` owes lesson M1 a criterion.** `round-95.md` M1 records `captured-by: none`
   and the durable fix ("re-read each target clause against one development run before the freeze")
   lives only in the plan/lesson; `LEARNING.md` step 3 requires a `QUALITY.md` criterion citing the
   lesson when no criterion caught the mistake — add one (or state why the checklist is its home).
3. **C2's void clause has a dead pointer.** SCORECARD/plan A2 say "void if
   `check-registry-coverage.py` differs from the hash in the C2 receipt"; no round-95 receipt records
   that hash. Record it (I measure `6fcb2d0a5f1b…` at the tip) in a receipt, or bind the guard to
   `git diff <pre-round>..<tip> -- tools/check-registry-coverage.py` being empty.
4. **Superseded superlative left standing in frozen tool docstrings.** `tools/limine-pin-battery-r95.py`
   (`fam_refusal_versions_9digit` docstring) and `tools/make-r95-bends.py` (header) still say "the
   largest in-bound member"; A3/ReviewBattery F1 established that is false under the per-component
   cap. Correct in a new commit and say how the r95 freeze manifest relates to the edited bytes.
5. **`corpus/README.md` A4 over-scope.** "the before instrument has no in-bound 9-digit case" is
   false for the whole instrument: the r94 `usage_check()` sends `999999999.0.0` (expected rc 0).
   Scope the sentence to the family roster (A4's own wording).
6. **Derived, not measured, C2 revisions.** The report lists `0afeb7d9` and `b8f878c8` as registry
   PASS points; the receipts exist only through `a302e688`. Mark the tip value derived (registry
   inputs unchanged) or commit a tip receipt.
7. **Carried, not new**: the `12.9.6.1` extra-component shape, the era-mechanism/echoed-version
   assertions (M06 survivor), the registry gate's lack of name→path/content binding, the per-component
   accepted family (Y/Z) — all Frontier rows in `corpus/README.md`; the kaidoku/revenger ownership
   stays operator-owned and unruled.

**SHONEN note for the operator**: all four boxes are `[~]`; boxes 2 (end-to-end task: the battery
certification run) and 4 (no cross-domain bleed: connector scan) look re-derivable by a non-author
from the committed evidence, but box 1 (whole-`SKILL.md` review) and box 3 (no-oral-context retest)
have not been executed by anyone, so the checklist is not fully non-author-checkable yet and
promotion stays operator-owned.
