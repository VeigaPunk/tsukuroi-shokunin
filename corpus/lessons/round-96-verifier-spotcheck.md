# Round 96 verifier spot-check — tsukuroi

author: hyaku closure (non-author integrator, @m_zfl)

## Conformance (step 1)

- Report `.ufo/reports/round-96/tsukuroi.md` committed in the fleet repo by the lane identity:
  `git log --format='%an %H' -- .ufo/reports/round-96/tsukuroi.md` → `tsukuroi-shokunin 42e6b55913b8873bb1d99aa4aecc688a59034217 round-96: tsukuroi report`.
- Report carries the `## SHONEN` heading with one line per box (4 lines, all `[~]` with evidence
  pointers); `## Work performed`, `## Landed changes`, `## Before → after measurements`,
  `## Sources & frontier`, `## Trend verdicts` all present.
- Cited lane commits exist and are ancestors of `master` (`git merge-base --is-ancestor`):
  `73c47107` (pre-round) OK, `c6786148` (post-round) OK.
- Lane HEAD `c6786148` == `git ls-remote origin refs/heads/master` → pushed. `jj-lane.sh state`
  → `ahead=0 behind=0` (untracked=1: `?? .ufo/waves/round-96/after/registry-final.json` — left
  uncommitted by the lane; receipt-shaped, not round work; named here as a leftover, not a blocker).
- Prompt `.ufo/prompts/tsukuroi-round-96.md` carries the template contract (§2 claims, §2b
  frontier, §3 L2 floor, §4 report contract, §5 commit/push scope, §6 hyaku addendum).
- Marker rule: the report names real committed work (9 lane commits, evidence pointers, a
  measurable `c6786148`) — not a marker.
- Verdict: conformant. Defects named below are status-neutral.

## Per-claim re-check

### C1 — depth 8 (roster 99 → 103)

- Commands run by the closure judge against committed bytes:
  - `python3 -c json.load(open('.ufo/waves/round-96/after/c1/gate-canonical.json'))` →
    3 runs, each `met 103 failed []`. **Re-measured.**
  - Independent re-run `python3 tools/limine-pin-battery-r96.py --gate tools/check-limine-pins.py
    --runs 3 --work /tmp/c1-rerun --json /tmp/c1-rerun.json` → exit 0; parsed verdicts
    `[('met', 103, []), ('met', 103, []), ('met', 103, [])]`. **Re-executed (closure judge).**
  - Bend receipts parsed: N01 `102 ["EXPLICIT-VERSION-ECHO"]`, N02 `102
    ["REFUSAL-VERSIONS-9DIGIT-Y"]`, N03 `102 ["EXPLICIT-VERSION-ERA"]`, N04 `101
    ["EXTRA-COMPONENT","REFUSAL-VERSIONS"]` — each ×3, matching the report.
  - Error-row check (judge count over `case_log`): landed `0`; N01 `0`; N02 `4` (all
    `bad-output: JSONDecodeError rc=64 stderr=usage: gate.py [-h]` — the bend's own refusals).
    A3 names these and narrows the frozen 0-error clause. **Report claim verified.**
  - Do-nothing: `dn-gate.json` 3× `met 99 []`; `dn-N04.json` 3× `unmet 98 ["REFUSAL-VERSIONS"]`.
  - `sha256sum -c .ufo/waves/round-96/before/instruments.sha256` → 17 OK, 0 FAILED at scoring.
  - Gate bytes unchanged: `git diff 73c47107..c6786148 -- tools/check-limine-pins.py | wc -l` → 0.
- Stated verdict-met on A3+A4 confirmed: A4 narrows the discrimination delta to three families
  (EXTRA-COMPONENT is a QUALITY 136 twin); A3 scopes the 0-error clause. Live with the report.
- Axis verdict: depth **unchanged** (8 → 8, sharper instrument).

### C2 — calibration 9 (F1–F6 → 0)

- `python3 tools/check-r96-calibration.py --selftest` (re-run by the closure judge) →
  `selftest PASS 7/7`. **Re-executed.**
- Committed receipts parsed: `before/c2-before-73c47107.json` → `FAIL`, 10 findings, ids
  F1–F6; `after/c2-after-landed.json` → `PASS`, `findings []`. **Evidence-verified.**
- One-fault fixtures fire exactly their own id (A1) — committed `w1/ExecControls/` receipts;
  not re-executed by the closure judge (sibling-gate evidence rule).
- A5 names the limit: the checker asserts six remedy conditions; only F6 binds a number, and
  only the first numeric occurrence. **Report claim verified.**
- Axis verdict: calibration **unchanged** (9 → 9, assurance repair).

### Gate-standard binding

Neither claim rests on a mutable-fleet-artifact gate verdict (no frozen-run verdict over a
mutable artifact is claimed as measurement). Both claims were **re-measured** (C1 by the judge's
own battery run; both by the judge's own receipt parsing + selftest re-run). C2's one-fault
and bend legs were **evidence-verified** against committed receipts under frozen instruments.

### Falsification ledger (2b)

- `python3 /home/vgpnk/Projects/shokunin/scripts/hyaku/prefile-falsification.py --lane tsukuroi
  --round 96` → `PREFILE-FALSIFICATION: pass claims=2 rows=11 attack_seats=5 findings=0`, exit 0.
- Ledger (`.ufo/waves/round-96/claim-falsification.tsv`): 11 rows — 3 falsifies-wording, 1
  falsifies-number, 7 neutral — covering claims C1 and C2 and all five attack seats
  (`ReviewBattery`, `ReviewCalibration`, `CriticClaims`, `MutBound`, `ConnectorOverlap`).
  Each wording/number row names an existing wave artifact and the amendment that narrows it
  (A3/A4/A5 in `before/plan-amendments-A1-A2.md`). **PASS, no adjudication required.**
- Amendments A1–A5 verified present in `before/plan-amendments-A1-A2.md`.

## Discernment spot-check (LEARNING.md)

Re-opened sources (closure judge, 2026-11-08):

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S391 (new; supersedes S390) | admit | `https://docs.python.org/3.15/library/sys.html#sys.int_info.default_max_str_digits` (fetched: HTTP 200, 280632 bytes, sha256 `a7e00587…` — matches the pin) | agree | Quoted sentence found verbatim at byte 157851 (after the code element split); ≤25-word quote; the row grounds the per-component cap claim; no Limine behaviour asserted. |
| S389 (re-open) | admit | `https://docs.python.org/3.15/library/stdtypes.html` (fetched: HTTP 200, 815447 bytes, sha256 `6bf2ce2b…` — matches the pin) | agree | "The default limit is 4300 digits…" found at byte 785297 as cited; byte-identical to the r95 pin; supports the gate's 1–9-digit cap. |
| `https://man.archlinux.org/man/limine.8` | reject | judge re-fetch: HTTP 404, 2706 bytes, title "Page not found — Arch manual pages" | agree | No such page; no behaviour stated; refusal recorded with evidence. |
| `api.github.com/.../tags/v12.9.6` | reject | lesson records HTTP 200, 26652 bytes, body 512 bytes pointing at the ChangeLog | agree | Locator, not behaviour evidence; correctly kept out of the registry. |

- `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` →
  exit 0, 0 E findings, 57 W04 + 1 W01 (census taken by the closure judge; matches the
  report's 58 W count).
- Census before → after: 389 → 391 (`git show 73c47107:corpus/SOURCES.md | grep -cE
  '^\|[[:space:]]*S[0-9]{3,}'` → 389; tip → 391). Rows added: two A (S390, S391
  superseding it per CORPUS.md rule 2). S390 status/used-by moved mined→queued / entry→`—`
  (logged in the lesson). **Standing spot-check verdict: discernment unchanged.**

## Trend verdicts

- **expansion — unchanged.** S390 + S391 (two A rows; S391 superseding S390 under rule 2) plus
  the knowledge entry `corpus/knowledge/limine-bound-per-component-r96.md` (frontmatter trio
  present — `source:` cites S389 and S391). The quote is verbatim at the cited byte; the lane
  corrected its own wrong anchor by supersession with a fail-before/pass-after checker. No
  admission bar failure found → not harmed. The judge does not certify "improved" on the
  coverage-map claim a gene-checker re-derived, but the admitted entry on ground the map did
  not hold (per-component cap + gate metadata) is on record.
- **quality — unchanged.** Six routed r95 self-assessment defects closed with a re-runnable
  counter (before six classes present, after zero, selftest 7/7); registry `PASS 154/154`
  at `c6786148` (re-read at `after/registry-final.json`, status PASS, findings 0); the r95
  docstring/README false statements corrected with their manifest relation stated; gate bytes
  unchanged and the r95 roster still reads 99/99 met on the landed gate. No admitted entry
  fails its re-check. No score uplift claimed and none certified.
- **discernment — unchanged.** The lane's own wave seats produced six narrowings (A1–A5 plus the
  F-4 docstring routing) and three named survivors (M06/M07/M08, F-E/F-G); the capsule's own
  errors (frozen 0-error clause, EXTRA twin, remedy-checklist wording, checker drift) are filed
  as mistakes in the lesson. The judge's re-open of the S391/S389 admits and the two reject
  decisions agrees with the lane's gate on all four samples above. Unlearned disagreements: none
  found.

At least one admit and one reject were re-opened and agree.

## Axis verdicts (match the MANIFEST entry)

| axis | verdict |
|---|---|
| depth | unchanged |
| coverage | unchanged |
| operability | unchanged |
| freshness | unchanged |
| calibration | unchanged |
| adjacency | unchanged |

No axis harmed (`git diff 73c47107 c6786148 -- SCORECARD.md` and spot reads: scores stable,
the gate bytes are unchanged, corpus additive).

## Routed defects (lane to fix next round)

1. **r96 untracked receipt** — `.ufo/waves/round-96/after/registry-final.json` is left
   uncommitted in the lane repo (`??` status). Read the registry receipt at `c6786148` by
   the closure judge; leave it for the lane to commit or discard next round.
2. **r96 docstring frontier** — the Y-family docstring's era claim is false (an X-only era
   reader passes Y and fails ERA); frozen bytes were not edited (C1 void clause). Lane owes:
   a docstring correction with its own manifest (already routed to r97 in the lesson).
3. **r96 Y-docstring (carried)** — same correction as (2).

## STANDING VERDICT (do not certify expansion or quality improved)

At least one admission and one rejection were spot-checked with re-opened sources; the lane's
gate agrees with the judge's sample 4/4. Sample verdicts: **each of the three trends above
grades `unchanged` on this judge's sample.**

[Claim-verification rows omitted: both claims verified (C1 re-measured including an independent
103/103 battery re-run; C2 selftest re-executed + receipts evidence-verified).]

**Bottom line:** This round's expansion is **unchanged** and quality is **unchanged** on the
judge's sample.
