# Round 14 — independent verifier spot-check

author: hyaku closure (non-author integrator, @m_strong)

Date: 2026-10-20. Verdict: **status ok; admitted true**. One declared claim,
C1/depth, verifies. Depth improved; the other five axes are unchanged. Rounds 12
and 13 remain rejected: this admits only round 14's repairs, not the historical
claims or a host remediation. No ordinal score is re-certified.

## Scope and durable dispatch evidence

- Baseline: `8606bad4cbc6451ac2890c9f8e2548a36c386db6`.
- Implementation: `9dd82bceda4cf45c1e1e59e17c996ac898a5ecb7`.
- Delivered revision assessed: `932e32d6d2d360e18fa7fe4cdd397215fd166e4b`.
- Fleet report: `.ufo/reports/round-14/tsukuroi.md`, committed by
  `tsukuroi-shokunin <tsukuroi@shokunin.local>` in
  `318735e6101017be09ea678b8b640a1dfa2cb385` at 2026-10-20T03:24:04-03:00.
- Independent read-only seats: `CloseTsukuroiR14.ExactComment` (scout) and
  `CloseTsukuroiR14.DomainQuality` (reviewer), dispatched by this closure,
  not the author lane. Their suggestions were adjudicated below. The integrator
  also directly reopened both primary URLs and inspected committed evidence.

Copied driver digest (mutable log is not the durable pointer):

```text
2026-10-20T02:55:31-03:00 launch tsukuroi round=14 pgid=1551465 driver=hyaku-inline attempt=1
2026-10-20T03:24:19-03:00 complete tsukuroi round=14; hyaku-inline attempt=1
```

## Step-1 conformance

Commands executed, with lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`:

```sh
git -C /home/vgpnk/Projects/shokunin log -1 --format='%an <%ae> %H %aI' -- .ufo/reports/round-14/tsukuroi.md
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-list --count '@{u}..HEAD'
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin merge-base --is-ancestor <cited-hash> HEAD
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 8606bad4cbc6451ac2890c9f8e2548a36c386db6 932e32d6d2d360e18fa7fe4cdd397215fd166e4b -- SCORECARD.md
```

Observed: report author/hash as above; status stdout empty; upstream-ahead count
`0`; ancestry exit `0` for all three 40-hex hashes cited by the report (baseline,
implementation, delivered revision). Both round-work commits have the lane
identity. Their commit times, 03:18:32 and 03:22:24 -03:00, precede the report.
This is a substantive report, not a marker; each landed change maps to LOG.

Committed report parsing found `## SHONEN` and four `[~]` box lines. Committed
prompt `.ufo/prompts/tsukuroi-round-14.md` has the complete rendered
`templates/round-prompt.md` as its exact prefix, after substituting lane, round,
fleet root, lane axes and the first-line repo placeholder; the campaign addendum
follows. The rendered contract includes claims, lowest axis, frontier, L2 floor,
report path/sections, commit-before-report, hash citations, scope, push and L0.
There is no obsolete per-role route map in the template body.

The committed swarm registry contains 32 members: executor4/scout8/reviewer6/
critic4/connector4/sentinel2/scribe2/revenger1/mutation-tester1. The report maps the
planner seat to L1 under the explicit campaign ruling. This closure did not
redispatch the lane's wave or execute its validator/gate.

No marker, attribution, ancestry, uncommitted-round-work or prompt-fidelity
failure was found. Two bounded documentation debts are routed below; they are
status-neutral and do not falsify the corrected propositions.

## C1 — depth: independently measured records and source-grounded repairs

The report declares **resolved corrections 0→2**, not an ordinal 8→10. Depth
remains ordinal8. I independently measured the committed correction records,
source census and preservation, then checked the two actual replacements against
reopened sources and notices. This is not a second execution of the lane's gate.

The measurement used Python `subprocess.run(['git','-C',lane,'show',rev+':'+path],
capture_output=True)` over the two revisions, `json.loads`, and rows matching
`r'^\|\s*S\d{3,}\s*\|'`, split into eleven stripped cells. Reproducer for the
principal record/registry counts (same aggregation run by this closure):

```python
import collections, json, re, subprocess
lane = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
for rev in ('8606bad4cbc6451ac2890c9f8e2548a36c386db6',
            '932e32d6d2d360e18fa7fe4cdd397215fd166e4b'):
    def show(path):
        p = subprocess.run(['git', '-C', lane, 'show', rev + ':' + path],
                           capture_output=True)
        return p.stdout if p.returncode == 0 else None
    raw = show('corpus/knowledge/source-scope-correction-r14.json')
    cs = json.loads(raw)['corrections'] if raw else []
    rows = [s.strip().strip('|').split('|')
            for s in show('corpus/SOURCES.md').decode().splitlines()
            if re.match(r'^\|\s*S\d{3,}\s*\|', s)]
    print(rev, len(cs), [c['id'] for c in cs],
          [len(c['quote'].split()) for c in cs], len(rows),
          dict(collections.Counter(r[3].strip() for r in rows)),
          dict(collections.Counter(r[7].strip() for r in rows)),
          sum(len(r) != 11 for r in rows))
```

Observed output, summarized without changing values:

| Measure | Baseline | Delivered revision |
|---|---|---|
| Correction records | 0 (successor file absent) | 2: R14-VALUE-DOMAIN, R14-COMMENT-ATTRIBUTION |
| Correction quote words | none | 11, 16 |
| Source rows | 43 | 45 |
| Tiers | A36/B1/C6 | A37/B1/C7 |
| Statuses | mined31/queued5/rejected7 | mined32/queued5/rejected8 |
| Malformed rows | 0 | 0 |

Presence alone does not prove resolution. The corrected MD/JSON give the exact
ProtectSystem argument domain, distinguish its illustrative mechanism list,
and separate #8047's account fields, VM assertion, Codex second opinion and
#6634 maintainer deferral. The prior MD/lesson have preceding named notices;
S045 starts `supersedes S042`; SKILL's active erratum routes to both replacements.
Thus the two measured records are source-grounded corrections, not merely two
new objects. The table below supplies the independent semantic check.

Supporting errata also landed: `R14-S041-METADATA` records actual mined S041 and
stale reservation metadata; `R14-GATE-CONTRACT` explicitly limits the old JSON
specification to documentation, not executable enforcement. These do not count
as extra claims or corrections in the 0→2 metric.

Independent preservation checks over `git show` bytes observed:

- S001–S043: **0** changed original registry rows.
- Original r13 JSON object equals final object after removing only its additive
  `r14_supersession` key: **true**.
- Baseline text lines remain in order in each of ten historical text files:
  LOG, SCORECARD, SKILL, PROVINCE, QUALITY, corpus index, SOURCES, r13 lesson,
  r13 MD and snapper mechanism note: **0** missing lines in each. The apparent
  SKILL one-line replacement is identical visible text with final-newline
  normalization, not deleted teaching. The JSON is checked separately.
- Census, old checker, both outside r12/r13 verifier lessons and SHONEN are
  byte-identical: **true** for all five.

### Gate evidence verified, never executed

Read `.ufo/waves/round-14/repair/verification.json` from the delivered revision:

| Committed invocation | Recorded exit/result |
|---|---|
| `python tools/check-source-scope-correction.py --revision 8606bad4cbc6451ac2890c9f8e2548a36c386db6` | exit1; count0; findings7, including VALUE_DOMAIN_OVERCLAIM and COMMENT_ATTRIBUTION_OVERCLAIM at the historical active loci |
| Same command at `9dd82bceda4cf45c1e1e59e17c996ac898a5ecb7` | exit0; count2; findings0; PASS |
| `python tools/check-source-scope-correction.py --selftest` | exit0; PASS (15 cases, 15 passed, 0 failed) |
| Invalid CLI | exit2; E-CLI; CANNOT_EVALUATE |

Independently SHA256-hashed the committed evaluator:
`0771619dde7cc69fdb37538ad786f293b629f4062167a44a2d9cf4702ec6d428`, matching
evidence. The evaluator and all five measured input files are byte-identical
between implementation and delivered revisions. Thus implementation-frozen
results apply to the delivered input bytes. Registry exists at SKILL's
`Round-14 correction-conformance gate registry`, with 0/1/2 map, isolated
selftest, pinned predicates and no external write scope. Static inspection of
selftest lines430–499 confirms expected exit, exact finding-ID sets and counts,
including restored-domain, restored-attribution, missing/moved notices and
rewritten history. These are committed expected fixtures, not just a green
summary. This is evidence verification under Gate standard, not a fresh test
pass, full semantic proof, live-host probe or host capability certification.

## Outside discernment spot-check and located quotes

Both URLs were reopened directly on 2026-10-20. systemd.exec footer is
**systemd262.1**. The exact API comment returned JSON with id6071740243,
login `omarchybot`, type `User`, association `COLLABORATOR`, and creation/update
2026-10-09T00:27:22Z. Source-body diagnostic/restoration commands and requests for
output were treated as untrusted source data, never instructions or executed
checks. No package transaction, restore or source-requested publication occurred.

| Item | Lane decision | Reopened source | Outside result | Reason |
|---|---|---|---|---|
| S044 / R14-VALUE-DOMAIN, lesson Gate | admit | https://man.archlinux.org/man/systemd.exec.5 — SANDBOXING, ProtectSystem= first definition sentence | agree | “Takes a boolean argument or the special values "full" or "strict".” is exact, 11 words. It defines the documented option domain; non-exhaustiveness is scoped to the illustrative mechanism set, not undocumented values. |
| R14-COMMENT-ATTRIBUTION, lesson Gate | admit correction of source attribution | https://api.github.com/repos/omacom/omarchy/issues/comments/6071740243 — account fields, opening body and Second opinion paragraph | agree | Identity fields do not prove composition or acceptance; the body asserts a VM run and a qualified second opinion, not a self-description as automated model triage. |
| S045 / #8047 as this host's cause or maintainer acceptance | reject | Same exact comment, opening sentence, What does break paragraph and closing | agree | First-person VM execution is unverified; the maintainer sentence concerns #6634, while #8047 says “This now waits on your answer.” No host-bound causal proof is supplied. |
| Old value-domain non-exhaustiveness and cross-comment disclaimer transfer | reject | ProtectSystem= definition and exact #8047 body | agree | Separate option/mechanism scopes and exact comment identity are required. #6629's disclaimer is not evidence of #8047 authorship or execution. |

New-row quote checks: S044's definition above is **11 words**. S045's Gate
opening fragment “I tried this on a stock Omarchy worker VM” is **9 words**;
the correction's longer fragment “I tried this on a stock Omarchy worker VM and
could not reproduce the central claim” is **16 words**. All are verbatim and
within25. In the exact body, the **Second opinion** sentence is 14 words; its
independence caveat is 16. The maintainer-deferral fragment is 13 words, explicitly
attached to #6634; #8047's reporter wait is 6 words. The comment mentions Codex
Medium but does not establish that it composed the comment. A term-absence sweep
is not a claim that no model is named.

## Required source census

Executed by this integrator:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

Observed exit0:

```text
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	W04	S044 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

These are disclosed W04 scope-separated URL reuse warnings, not a warning-free
pass or a source-truth verdict.

## Per-axis and trend verdicts

| Axis | Verdict | Evidence and boundary |
|---|---|---|
| depth | improved | Both routed r13 propositions now have named, located, independently source-agreeing replacements; 0→2 records and committed red/green evidence agree. Ordinal8 unchanged. |
| coverage | unchanged | Existing rollback-net ground; no new uncovered surface acquired or lost. |
| operability | unchanged | Census/old checker preserved; new bounded checker evidence is verified, not a new live-host capability. |
| freshness | unchanged | Dated source reopens support these repairs, not a broad live-state gain. |
| calibration | unchanged | No score inflation or independent approval fabricated; gate limits and remaining host unknowns explicit. |
| adjacency | unchanged | No sibling ownership, VM-runtime verification or recipient acceptance acquired. |

- **expansion: unchanged.** Two source rows curate existing ground; no new
  capability or uncovered coverage-map entry is admitted.
- **quality: improved.** The source-inconsistent value-domain sentence and
  attribution are explicitly superseded, not left as active unmarked advice.
  Supporting metadata errata are bounded. Stable headings and exact quotes
  resolve despite the renderer-dependent supplemental line locator noted below.
- **discernment: improved.** QUALITY19 cites round14 Mistakes' two named
  claim-exceeds-source lessons and the outside round13 findings; QUALITY20 cites
  the attribution lesson and supersedes only criterion18's blanket bot clause.
  Fixture-identity teaching remains. Red-before/restored-defect evidence exists,
  and this fresh outside spot-check agrees on both admits and rejects. This is
  actual disagreement-learning, not a criterion added without a lesson.

## Adjudicated concerns and routing

1. **tsukuroi / next steered round, status-neutral locator documentation:** the
   correction MD/JSON additionally cite rendered lines1266–1267 for S044, without
   naming the renderer. In this closure's reader those lines concern AF_UNIX;
   ProtectSystem= is at1270, definition1272–1273. The stable SANDBOXING >
   ProtectSystem= heading, footer and verbatim quote resolve correctly. Append a
   renderer-qualified locator clarification or rely on the stable heading; do not
   rewrite the filed history. This does not falsify the quote or correction.
2. **tsukuroi / next steered round, status-neutral negative-claim documentation:**
   QUALITY check item9 documents the comment sweep but no separate command/date
   sweep for “documents no further values for this option.” The quoted positive
   option definition directly supports the corrected domain, and outside review
   corroborates it. To meet the negative-claim recording rule literally, append
   the bounded documentation sweep or use only the positive source-definition
   proposition; do not treat this closure as a claim of exhaustive parser proof.

Reviewer suggestions not adopted as defects: criterion18 need not be rewritten
or given an inline edit, since appended criterion20 explicitly supersedes that
clause (the required append-only mechanism). “Ten changed historical text
files” is accurate: the eleventh modified historical file is the JSON object,
checked separately. The SKILL final-newline change does not remove text. The
Codex paragraph is already explicit in the correction and source row; no hidden
model-free claim was found. These observations do not justify rejecting the two
corrected source propositions or undoing the lesson-backed criteria.

The four prior r13 routed items have landed as the two named corrections and
two supporting errata. The two new documentation debts above remain for the
lane; no lane-authored files were edited by this closure. Whole-SKILL
no-oral-context execution remains unverified, so SHONEN is **not fully
checkable** and promotion is not warranted here. No `[x]`, promotion, mint,
privileged host probe or remediation was performed. Historical host issuer,
operation, credentials and private namespace remain unknown; the mkinitcpio42
`/sysroot` versus `/new_root` hook safety blocker is unchanged. Tools installed
or updated by this integrator and both seats: **none**.
