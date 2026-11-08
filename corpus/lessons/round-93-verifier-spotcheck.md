# Round 93 verifier spot-check — tsukuroi lane

author: hyaku closure (non-author integrator, @m_zfl)

Lane HEAD before: `e406aa96b57e0aab2c7866f217b2e888bec535bb`; after (measured): `42979f5a2eb16babb4de344c5b21205accae2171`.
Driver digest (from the closure brief): `2026-11-08T02:52:56-03:00 launch tsukuroi round=93 pgid=2091834 driver=hyaku-inline attempt=1`; `2026-11-08T03:38:51-03:00 complete tsukuroi round=93; hyaku-inline attempt=1`.

## 1. Conformance (step 1)

- **Report landing**: `git log --format='%an %H' -- .ufo/reports/round-93/tsukuroi.md` in the fleet repo → `tsukuroi-shokunin a29c6f…` (the lane identity committed it). Pass.
- **`SHONEN` heading**: present, plus one `[~]` line per box (4 boxes). Pass. (All assert-by-author; the promotion gate is owed the closure, which this artifact is.)
- **Cited lane commits exist and are ancestors of `master`**: `merge-base --is-ancestor` → `c633f49a` (freeze), `b02384c7`, `9f66744e`, `42979f5a` all `ok`; the pre-round `e406aa96` is an ancestor of the post-round tip. Pass.
- **Clean lane worktree, pushed**: `jj-lane.sh state` → `ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` in the lane repo → empty (no uncommitted round work). Pass.
- **Prompt contract**: `.ufo/prompts/tsukuroi-round-93.md` (989 lines, committed by `tsukuroi-shokunin 2b32bf36…`) carries the template contract. Pass.
- **Not a marker**: the report names a real committed round-work hash (`42979f5a`) plus evidence pointers, changes landed and tied to a `LOG.md` entry. Status `ok`.
- **`git log` in the closure brief vs. measured ancestry**: the brief's `HEAD` may be detached; all ancestry checks above run against the `master` ref, per the brief. No `@{u}` test used.

## 2. Claims — re-derive (plain measurement, run by the closure)

Commands are run inside `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Receipts under `.ufo/waves/round-93/after/` (canonical + `clone-gate.json` / `clone-bend-N01…N04.json`) and, for the C2 clone bends, `w1/ExecAutoReplicate/{n05,n06}.json`.

### C1 — depth 8 (tied lowest non-retired axis) — VERIFIED, re-measured

Claim (amendments A1-A3 narrowed wording): `limine-pins` battery carries `ERA-EXACT-125`, `ERA-B-FIRST-BODY`, `ERA-B-U1`, `REFUSAL-VERSIONS`; landed gate reads `96/96 met ×3` canonical and `×3` in a `git clone --shared`; N01-N04 each `unmet ×3` both layouts with the named family in `failed_families` and 0 error rows.

Observed (re-derived from the receipts, not copied from the summary):

| receipt | runs | verdict | passed | failed_families | 0 error rows |
|---|---|---|---|---|---|
| `after/c1-canonical.json` | 3 | `met` ×3 | 96/96 each | `[]` | yes — recomputed from `case_log` |
| `after/clone-gate.json` (clone HEAD `c633f49a`) | 3 | `met` ×3 | 96/96 each | `[]` | yes |
| `after/bend-N01-exact-split.json` | 3 | `unmet` ×3 | 95/96 | `ERA-EXACT-125` | yes |
| `after/bend-N02-first-body.json` | 3 | `unmet` ×3 | 88/96 | 8 incl. named `ERA-B-FIRST-BODY` (+7 collateral) | yes |
| `after/bend-N03-era-b-u1.json` | 3 | `unmet` ×3 | 95/96 | `ERA-B-U1` | yes |
| `after/bend-N04-accept-any.json` | 3 | `unmet` ×3 | 95/96 | `REFUSAL-VERSIONS` | yes |
| `after/clone-bend-N01…N04.json` | 3 each | `unmet` ×3 each | 95/88/95/95 | same four families | yes |

Before-leg: `grep -c "ERA-EXACT-125\|ERA-B-FIRST-BODY\|ERA-B-U1\|REFUSAL-VERSIONS\|AUTO-ERA-A\|AUTO-ERA-B\|AUTO-PROBE-FAIL" before/controls/do-nothing-battery-r92.py` → `0`; the r92 battery scores the landed gate `89/89 met` (`after/r92-battery-on-r93-gate.json`, single run, 0 error rows). Matches the reported `89/89`. Commands used: `jq`-equivalent Python parse of each JSON (`families_passed`, `failed_families`, full `case_log` recompute of pass counts and of the error rows) plus `grep -c` on the control battery. **Verdict: met (verified by re-measurement).**

### C2 — operability 9 (assurance arm + capability `installed-version-probe`) — VERIFIED, with evidence substitution noted

Claim: `--limine-version auto` probes the installed bootloader read-only, records `limine_version`/`limine_version_source`, selects the era from the probed value, refuses on the certified failure shapes; `AUTO-ERA-A`, `AUTO-ERA-B`, `AUTO-PROBE-FAIL` `met` in every run; N05/N06 `unmet ×3` both layouts; live receipts show `12.9.4`/`probe`.

Observed:

| receipt | observation |
|---|---|
| `after/c1-canonical.json` + `after/clone-gate.json` | All 6 runs pass the three AUTO families `4/4` each (per-family matrix `after/bend-family-matrix.txt`). Matches "4/4 in every run". |
| `after/bend-N05-auto-ignore.json` | 3 runs `unmet`, 95/96, `failed_families: ['AUTO-ERA-B']` alone, 0 error rows. |
| `after/bend-N06-auto-fallback.json` | 3 runs `unmet`, 95/96, `failed_families: ['AUTO-PROBE-FAIL']` alone, 0 error rows. |
| `w1/ExecAutoReplicate/n05.json`, `n06.json` | Clone legs: 3 runs each, `unmet` ×3, 95/96, the same single family, 0 error rows. (These two files are the only C2 clone ×3 receipts; the report cites them, correctly — they are not under `after/`.) |
| `after/live-c2.json` | Single-line JSON: `"limine_version": "12.9.4"`, `"limine_version_source": "probe"`, `rc 1` / `DEGRADED`, `visibility_era pre-12.9.5`, `findings ["LP-MISMATCH line 30", "LP-MISMATCH line 38"]`, 5 pins. Cross-checked against `w1/ExecLive/era-selection.json` and the strace receipt. |
| `after/c2-donothing-r92-gate.json` | Single-run dict (not a ×3 list): `94/96 unmet`, `failed_families: ['AUTO-ERA-A', 'AUTO-ERA-B']`, 8 error rows (all `JSONDecodeError rc=64` inside the two AUTO families); `AUTO-PROBE-FAIL` passes. Matches Amendment A1's narrowed control sentence verbatim. |

**Verdict: met (verified by re-measurement of the receipts; mechanism evidence verified, not re-executed — see §2b).**

**Evidence substitution, stated plainly.** The C1/C2 numbers above are re-measures *of the frozen receipts* (fresh counts over committed bytes), not re-runs of `limine-pin-battery-r93.py`. Per the Gate standard, the closure verifies a gate's committed evidence; it does not execute a sibling's gate. The battery selftest at the landing tip reads `selftest PASS 5/5` (`after/battery-selftest-noref.txt`), the gate selftest reads `PASS 39/39` (ExecLints), the registry-coverage receipt at `9f66744e` reads `PASS 147/147` (`after/registry-coverage-tip.json`), knowledge headers `109/109` and dangling refs `0` at the same revision (`after/knowledge-{header,refs}-tip.json`), and line endings `PASS (477 file(s) checked, 0 violation(s))` (`after/line-endings-tip.txt`). One recorded gap: the battery's 18-leg `--reference` run was NOT completed in the wave timebox (ExecLints F3 — a killed run proves nothing); the report discloses this and routes it. It does not falsify any C1/C2 number (all verified receipts re-derive without it).

### 2b. Pre-file falsification ledger (addendum §8)

Command: `python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tsukuroi --round 93` →

`PREFILE-FALSIFICATION: pass claims=2 rows=15 attack_seats=7 findings=0` (exit 0).

All 15 TSV rows read; every `falsifies-wording` row names a narrowing in `.ufo/plans/round-93.md` (A1-A4 all present; the plan's amendment text verified). **One count defect, status-neutral**: the report (§Pre-file falsification ledger) says "5 `falsifies-wording` rows", but the TSV contains **7** (`grep -c falsifies-wording claim-falsification.tsv` → `7`: 3 for C1 — ReviewBattery, ReviewGate, CriticClaims; 4 for C2 — MutAuto, CriticForgers, CriticClaims, ReviewGate). All 7 point at the plan and each amendment exists, so the substance holds and the claims still verify; only the count is stale (this is a report-prose correction, not a claim defect). Routed to the lane (§6).

## 3. Discernment spot-check (LEARNING.md, §Discernment checked from outside)

Live network re-opened at source and byte-compared against the committed pins in `.ufo/waves/round-93/w1/ScoutSource/pins/`.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S382 — Limine `common/lib/config.c` (v12.9.5) | admit | live `raw.githubusercontent.com …/v12.9.5/common/lib/config.c` (sha256 `a940acae…`), identical to the committed pin | **agree** | Quote `if (p > config_addr) { *(p - 1) = '\0'; }` at raw 328-330 inside `create_menu_tree()`; confirms the 12.9.5 (not 12.9.6) boundary. |
| S383 — Limine ChangeLog (v12.9.5) | admit | live `…/v12.9.5/ChangeLog` (sha256 `d2e08cc4…`), identical to the pin | **agree** | Quote `Parse the config in linear time…` at raw 8-9 under the 12.9.5 release head. |
| S384 — Limine `host/limine.c` (v12.9.5) | admit | live `…/v12.9.5/host/limine.c` (sha256 `4da21c7c…`), identical to the pin | **agree** | `puts("Limine " LIMINE_VERSION);` at raw 2035 (M4's corrected locator — raw 2029 is blank); `--version` dispatch at 2089-2091. |
| `api.github.com …/git/trees/v12.9.5?recursive=1` | reject | live HTTP 200; byte-identical to `before/src/tree-v12.9.5.json` | **agree** | Directory listing locates S384 but states no behaviour; correctly kept as a wave-dir locator, not a SOURCES row. |
| `…/common/lib/misc.c` (v12.9.5) | reject | live HTTP 200 (sha256 `3b81e321…`), identical to the pin | **agree** | Negative locator confirmed: 0 occurrences of `Limine ` / `--version` / `LIMINE_VERSION` on the version path. |

**SOURCES census**: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 0, 385 rows (`381 → 385` vs the pre-round revision verified by `git show e406aa96:corpus/SOURCES.md | grep -c '^| S'` → 381; the tip reads 385). The census prints only the standing W04 duplicate-URL warnings and one W01 (tier-C mined, pre-existing). Newly-written rows S382-S385 are all tier A / `mined`, consistent with the report.

**Rule-1 gap (defect, routed)**: `CORPUS.md` §SOURCES.md rule 1 requires the round lesson's `## Gate` to record, *for every new row*, the URL, the access date, and a ≤25-word located quote. S385 (the version-pinned Python docs supersession of S377) is new in r93 but has no row in the r93 `## Gate` table (lesson lines 7-11 list S382-S384 only); the two prose mentions carry no URL/date/quote. The S385 anchor and sha256 are correct (live byte-compare: sha `d3c503060…` matches the row), so this is a Gate-recording debt, not a sourcing error. Routed in §6.

## 4. Axis verdicts (vs. the scored diff `e406aa96…42979f5a`)

No axis score moved (SCORECARD axes stay `depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8`); the per-claim verdicts are therefore carried on measured receipts, not ordinals.

| axis | verdict |
|---|---|
| depth (C1) | **improved** — four sourced families added; landed gate `96/96 met ×3` both layouts; each bend kills exactly its named family (`95/88/95/95`, 0 error rows) plus one bounded collateral on N02 that the report discloses. Re-measured from the receipts. |
| operability (C2) | **improved** — the `--limine-version auto` probe arm lands with the `installed-version-probe` capability (first-working round 93, live receipts `12.9.4`/`probe`); the do-nothing honestly reads `94/96 unmet` with A1's narrowing accepted. Mechanism (read-only syscall trace, probe edge cases) verified from ExecLive receipts, not re-executed by the closure. |
| coverage | **unchanged** — no ordinal move claimed; the round stayed on the owned Limine surface and gained new rows (S382-S385) plus one knowledge entry, but no new surface class. |
| freshness | **improved** — S377 and S384 anchor corrections landed with sweep receipts (`after/q127-s377-{pre,landing}.txt`, `after/s384-line-receipt.txt`); census 385 exit 0. |
| calibration | **improved** — 7 `falsifies-wording` rows all narrowed (A1-A3) rather than filed as claimed; the one report-level count staleness ("5 for 7", §2b) is the calibration miss of this closure, status-neutral. |
| adjacency | **unchanged** — ConnectorOverlap's 20-repo sweep found no contention, none claimed; the contested kaidoku/revenger RE ownership remains unruled (operator-owned). |

Claims verified: C1 met (re-measured), C2 met (receipts re-derived; mechanism evidence verified). No axis is `harmed` on the evidence above. No claim was exploratory; the round exercised no `unprovable` path.

## 5. Trends

- **expansion — improved.** One admitted knowledge entry on ground the coverage map did not hold (`corpus/knowledge/limine-version-probe-r93.md`) whose `source:` cites three `mined` rows opened this round (S382-S384) plus S385; SOURCES 381 → 385 (census exit 0). The census warnings are standing ones, not round-introduced.
- **quality — improved.** Seven new families each tied to a one-clause bend; the r92 survivor `N04-accept-any` is killed at family level; registry 147/147 and headers 109/109 at the landing revision; two anchor cells corrected with sweep receipts; the r92 battery still scores the new gate `89/89` (no regression). One honesty note: the registry-coverage FAIL at the freeze revision was RED in the wave and only repaired in SKILL.md at the landing commit — the landing receipts verify the repair (disclosed, not hidden).
- **discernment — improved.** The spot-check agrees with the gate on all three admits and both rejects (table §3), each with byte-located evidence; the attack seats falsified 7 wordings and the round narrowed them rather than filing them (A1-A3), and the survivor M13/M12/M03-M05/M11 mutants were routed rather than declared dead. The one S385 Gate-row gap (§3) is routed for the next round to close.

## 6. Routed defects (next round)

1. **Report prose count** (r93 report, §Pre-file): "5 `falsifies-wording` rows" vs the TSV's 7. Correction lands in the next round's report (reports are never rewritten) naming this. Status-neutral — every row's narrowing resolves to a plan amendment.
2. **S385 Gate row**: add the rule-1 row (URL, `2026-11-08`, ≤25-word located quote) in the next round's lesson before any future row cites S385. The row's sha, anchor and `mined` status are confirmed correct now.
3. **Unfinished battery `--reference` run**: run the 18-leg reference-backed battery leg (ExecLints F3) or carry the route forward; the closure verified every claimed number without it, so it is debt, not a defect against the claims.
4. **Surviving mutants** (from MutEra/MutAuto, disclosed): the 10-digit component cap (M13), the `AUTO` fake's source leakage (CriticForgers §3), and the M12 timeout error-row shape — name the narrowing or add the discriminators in a later round.
5. **Probe grammar leniency** (suffix / extra components — ReviewGate F1, CriticClaims §5): the first-`X.Y.Z` parse reads `12.9.6-rc1` as `12.9.6`; a release-format change is a re-pin of S384, noted in the lesson. Kept on the frontier.
6. **Contested scope**: kaidoku/revenger RE ownership remains unruled (operator-owned, not round debt). If the SHONEN boxes look fully checkable by a non-author, that decision stays with the operator.
