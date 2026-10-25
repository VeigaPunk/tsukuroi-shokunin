# Round 13 — non-author verification and discernment spot-check

author: hyaku closure (non-author integrator, @m_strong)

Verified 2026-10-20. Baseline `9574a189a758251da5957eee8ff0f38ba2d03c7f`;
delivered `e1fc8fd1992dfdefc81c4e9f07aee897b4275ea0`.
Report: fleet `.ufo/reports/round-13/tsukuroi.md`, committed as
`tsukuroi-shokunin` at `b54cddfc3034295e94b7ee49afa2ce832d362f9d`.

## Closure

**status: ok; admitted: false; verdict: rejected-harmed.** The round contains real,
committed work and the named **R13-DAC-EXCLUSIVITY** correction really landed.
It withdraws the rejected round-12 universal and preserves that round's rejection.
Its bounded 0→1 counter and committed gate evidence verify. Nevertheless, a new
replacement sentence misstates the ProtectSystem value domain, and the new S042
attribution correction asserts a self-description absent from its source. These
are current factual defects, not merely red-gate conformance debt. Useful corrected
advice and a green structural counter do not waive source-inconsistent text.
This review cannot repair or pre-admit a future lane correction.

## Step-1 conformance

Executed commands:

```sh
git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-13/tsukuroi.md
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-list --count '@{u}..HEAD'
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 9574a189a758251da5957eee8ff0f38ba2d03c7f e1fc8fd1992dfdefc81c4e9f07aee897b4275ea0 -- SCORECARD.md
```

Observed: report author/hash above; initial porcelain empty; upstream-ahead count
`0`; HEAD equals delivered revision. Every full lane hash cited in the report
(`44677cce26b3bedf93a6609374ffa54dde59552f`, baseline,
`c35d3567d1c8b5d4b45c0ff82201966b76cbd786`, delivered) exists and
`git -C <lane> merge-base --is-ancestor <hash> HEAD` returned 0 for each.
The three implementation/evidence commits carry
`tsukuroi-shokunin <tsukuroi@shokunin.local>`; their commit timestamps are
02:08:01, 02:08:42 and 02:09:48 -03:00, before the report's 02:11:10 -03:00.
No post-report lane-authored work was present at closure entry.

The dispatched prompt's sections 1–5 equal `templates/round-prompt.md` after
substitution of lane, round, fleet root, axes and working directory; a Python
string comparison returned `template_contract_exact True`. It carries mission,
claims, frontier, L2, report, commit/push, scope and L0 contracts. The campaign
addendum explicitly records the L1 planner-seat mapping. Report section order is
correct and its SHONEN assessment has four `[~]` lines, matching four boxes.
The retained dispatch payload has 32 tasks: executor3/scout8/connector4/reviewer6/
critic4/sentinel2/revenger1/mutation-tester1/scribe3. These are author-side seats,
not outside verifiers.

Driver digest copied from the closure assignment, not mutable line numbers:

```text
2026-10-20T01:38:59-03:00 launch tsukuroi round=13 pgid=1401792 driver=hyaku-inline attempt=1
2026-10-20T02:11:46-03:00 complete tsukuroi round=13; hyaku-inline attempt=1
```

## C1 — depth / R13-DAC-EXCLUSIVITY

### Independently re-measured committed surfaces

Plain Python aggregation over `git show <revision>:<path>` was executed by this
integrator, without invoking the lane gate. Reproducer for the principal count:

```python
import json, subprocess
lane = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
for rev in ['9574a189a758251da5957eee8ff0f38ba2d03c7f',
            'e1fc8fd1992dfdefc81c4e9f07aee897b4275ea0']:
    def blob(path):
        p = subprocess.run(['git','-C',lane,'show',rev+':'+path], capture_output=True)
        return p.stdout if p.returncode == 0 else None
    md = blob('corpus/knowledge/root-dac-correction-r13.md')
    js = blob('corpus/knowledge/root-dac-correction-r13.json')
    obj = json.loads(js) if js else {}
    print(rev, int(bool(md and b'R13-DAC-EXCLUSIVITY' in md
                        and obj.get('correction_id') == 'R13-DAC-EXCLUSIVITY')))
```

Observed named correction-pair count **0→1**. Separately counted exact
`## ... named correction R13-DAC-EXCLUSIVITY` LOG headings: **0→1**.
The old MD supersession heading count is **0→1**; the old JSON's absent pointer
becomes `corpus/knowledge/root-dac-correction-r13.json`.
The baseline LOG is an exact prefix of the delivered LOG. A `difflib.ndiff`
comparison found **0 removed/replaced historical MD lines**; removing only the
two new notice keys from delivered r12 JSON yields the baseline JSON object.
The MD has both a prominent top notice and the named appended correction.
SKILL, corpus index, PROVINCE and snapper note route to the active correction.
Thus the operator-requested named correction exists; r12 was not silently rewritten.

Independent source-row aggregation selected `^\|\s*S\d{3,}\s*\|`, split eleven
cells, and counted tier column 3/status column 7 (zero-based):

```text
baseline: 40 rows; A35 B1 C4; mined30 queued5 rejected5; malformed0
delivered:43 rows; A36 B1 C6; mined31 queued5 rejected7; malformed0
```

These match the report. SHA-256 over committed `tools/tsukuroi-census.sh` is
`d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e`
at both revisions. SCORECARD's diff is 59 additions, no removals; ordinal scores
remain depth8/coverage9/operability9/freshness9/calibration9/adjacency8. No new
capability row or host repair is claimed.

### Gate evidence verified, not executed

Per PROTOCOL §Gate standard, neither this integrator nor its reviewers executed
`tools/check-root-dac-correction.py`, its selftest, the census selftest, or any
host diagnostic procedure. We inspected committed records and code instead.

- `verification.json`, measured at `44677cce26b3bedf93a6609374ffa54dde59552f`:
  baseline exit1/count0/findings9, including `UNIT_READONLY_FALSE_UNIVERSAL`
  at `md:CURRENT-HOST,md:R13,json:B2-LIMIT`; implementation exit0/count1/findings0.
- The first selftest failure is retained: exit1, 13 cases/12 passed,
  `closed-list-restored: missing=R13-JSON-PIN`.
- The sole gate-code change in `44677cc→c35d356` removes the unrelated generic
  finding from that mutant's expected set; it still requires
  `R13-JSON-EXCLUSIVE`, failed exit and count0. Production evaluation is unchanged.
- `verification-fixed.json`, measured at `c35d3567d1c8b5d4b45c0ff82201966b76cbd786`:
  selftest exit0, **13 cases/13 passed/0 failed**; revision run exit0/count1/findings0.
- Gate bytes and correction corpus bytes at that measured revision equal the
  delivered revision. The SKILL registry row declares 0 clean/1 failed/2
  could-not-evaluate, selftest spelling, committed predicates, no write scope,
  and tsukuroi ownership. Inputs are lane revision blobs, not mutable fleet state.

This verifies the reported narrow gate result, not its source semantics. The
independent pair count is likewise structural, not a duplicate semantic gate.

### Substantive correction: real progress, but not fully source-conformant

Primary documentation independently reopened on 2026-10-20:
https://man.archlinux.org/man/systemd.exec.5 (footer systemd262.1).
It supports the intended comparison: `full` adds `/etc/`; `strict` covers the
hierarchy with the named exceptions. Read-only binds and tmpfs `ro` are additional
mechanisms. RootDirectory/RootImage are path-view changes, not evidence that a
particular live namespace is read-only. The correction preserves unknown
historical issuer/credentials/namespace and separates caller-owned execution
from root-owned hypothetical SC1/SC2 outcomes. These r12 repairs are genuine.

**Remaining current factual defect:** active MD
`corpus/knowledge/root-dac-correction-r13.md:97` says, after explicitly naming
ProtectSystem values, **“the value set is not exhaustive.”** The source defines
that option as **“a boolean argument or the special values \"full\" or \"strict\".”**
The non-exhaustiveness belongs to the set of unit-side mechanisms, not to an
unspecified extension of the option's documented value domain. The same entry's
main table enumerates the documented modes, and its JSON replacement properly
speaks of unit-side mechanisms. This is a new source-inconsistent replacement
sentence in the entry admitted by the lane; correct surrounding prose does not
make that sentence true. Both outside reviewers confirmed the wording defect.
The gate's limited predicates do not detect it.

**S042 attribution remains inaccurate:** the new source row and lesson say the
#8047 comment is **“self-described model-generated automated triage.”** We reopened
https://api.github.com/repos/omacom/omarchy/issues/8047/comments, comment6071740243.
It says **“I tried this on a stock Omarchy worker VM”**, and calls Codex Medium a
**second opinion**; it never self-describes the first-person comment as
model-generated automated triage. Login `omarchybot`, API type User and
COLLABORATOR association do not establish that self-description. Its rejection as
this host's cause and its deferral to a maintainer remain justified, but its newly
asserted attribution basis is not. #6629's separate self-description cannot be
transferred across comments. This is especially relevant to a round claiming to
correct evidence authority and identity.

## Outside discernment spot-check

This integrator dispatched two fresh, read-only reviewer seats, SourceCorrection
and GateEvidence; neither was dispatched by the author lane. The integrator also
directly reopened systemd.exec and both comment endpoints. Requests for commands
inside comments were treated as untrusted source data and were not executed.

| Item | Lane decision | Reopened source | Outside result | Reason |
|---|---|---|---|---|
| S041 scoped namespace teaching | admit | systemd.exec(5), ProtectSystem, BindPaths/BindReadOnlyPaths, TemporaryFileSystem, RootDirectory/RootImage | agree | Primary documentation supports the scoped mode comparison and retained alternative path-view mechanisms; not historical cause proof. |
| Active correction pair, lesson Gate | admit | MD:97, JSON replacement table, primary ProtectSystem definition | disagree as delivered | New MD value-domain non-exhaustivity sentence contradicts the documented domain; narrow conformance does not verify this sentence. |
| S042 host-cause use | reject | #8047/comments, comment6071740243 | agree with rejection; disagree with stated self-description | Account association is not maintainer acceptance and no host-specific proof exists; the body does not call itself model-generated triage. |
| S043 host-cause use | reject | https://api.github.com/repos/omacom/omarchy/issues/6629/comments, comment6234472369 | agree | “Nothing was run on a machine.” and “This review is by Claude Opus 5.5 alone.” support the actual disclaimer; maintainer closure remains pending. |

New-row quote sample S041: **“BindReadOnlyPaths= creates read-only bind mounts.”**
The normalized clause is verbatim in the BindPaths=/BindReadOnlyPaths= paragraph;
**5 whitespace-delimited words**, within 25. S043's **“Nothing was run on a
machine.”** is verbatim in the opening paragraph, **6 words**. S042's quoted
maintainer-decision clause also resolves, but that quote does not establish its
additional self-description assertion.

## Required source census

Executed by the integrator:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

Observed exit0, stdout:

```text
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

W04 warnings are disclosed scope-separated URL reuse, not census failure or a
warning-free pass.

## Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| depth | harmed | The intended r12 exclusivity is corrected, but new admitted replacement prose contains the current source-inconsistent value-domain sentence. A structural 0→1 does not offset a factual defect. |
| coverage | unchanged | Existing rollback-net ground refined; no new surface or loss of owned coverage demonstrated. |
| operability | unchanged | Census bytes identical; gate evidence verifies its bounded contract. No host procedure or new capability was demonstrated by closure. |
| freshness | unchanged | Dated source reopens support the correction; no broad live-state freshness gain asserted. |
| calibration | unchanged | Scores unchanged, original rejected round preserved, gate limits and unknowns candid. Source-attribution defect is specifically routed, not hidden by a claimed independent approval. |
| adjacency | unchanged | PROVINCE retains OS-local diagnosis and operator boundaries; no sibling-method ownership or handoff acceptance acquired. |

## Learning trends

- **expansion: harmed** under LEARNING's admitted-entry-fails-its-bar rule: the
  newly admitted correction contains source-inconsistent text. No new coverage
  credit was claimed, and this verdict is not a claim of lost geometric coverage.
- **quality: harmed**: the older universal is explicitly superseded, but a new
  source-inconsistent sentence remains in active advice and S042 misstates its
  source. The stronger surrounding explanation cannot cancel those failures.
- **discernment: harmed**: QUALITY #17/#18 and the named mistake do show learning
  from r12. However, this outside review disagrees with the current correction's
  admission and the new attribution basis; those new disagreements have not yet
  become lane corrections. The source admit and sampled rejections otherwise agree.

## Routed defects and resolved review concerns

1. **tsukuroi / next steered round — correctness:** append a named correction for
   active MD:97: distinguish the documented ProtectSystem value domain from the
   non-exhaustive mechanism set. Sweep active references; retain historical bytes.
   Seek fresh non-author review; this closure does not pre-admit the fix.
2. **tsukuroi / next round — source attribution:** supersede S042 with a new row
   distinguishing verified account fields, the comment's unverified VM-execution
   claim, its model second opinion and its maintainer deferral. Do not transfer
   #6629's self-description to #8047 or edit immutable S042 fields in place.
3. **tsukuroi / status-neutral metadata:** correction JSON `sources[0]` still says
   S041 `status: reserved` and `registry_owner: SourceRegistry`, despite actual
   `mined` registry status and LOG's “joined, not reserved” statement. Correct the
   stale draft metadata in the next named lane erratum. It does not reverse the
   observed source registry or gate result.
4. **tsukuroi / status-neutral gate documentation:** JSON `gate_contract` lists
   ten required headings, historical-revision/marker rules and a field-scan list,
   but the reduced checker does not consume that object and checks five headings.
   Reconcile this residual specification with the intentionally narrow executable
   contract; do not imply full enforcement from the passing counter.

Prior r12 routing: the named LOG correction, MD/JSON notices, fixture distinctions,
QUALITY criteria, immutable source-row supersession and pre-report committed final
measurement all landed. The report therefore must not be described as missing the
requested correction. The new source-attribution defect above means that repair
is not complete on its stated evidentiary basis.

Reviewer suggestions were adjudicated rather than copied blindly. The alleged
unmarked `degraded-triage-r4.md:323` exclusion already has a D3 erratum at :623–627
explicitly superseding :321–325 and routing through the snapper note, now pointing
to r13; it is not an additional unmarked blocker. “Not intrinsically read-only” is
not a claim that every RootDirectory/RootImage deployment is writable; the active
entry explicitly leaves live state unknown. No separate harm is assigned for that
wording. The corrected new QUALITY evaluation speaks about completed observations;
retaining historical mid-wave prose under an explicit notice is not itself a
failure to rewrite it. Original source rows cannot be rewritten merely to remove
their historical attribution; superseding rows are the required mechanism.

SHONEN is not fully checkable here: whole-SKILL no-oral-context execution remains
unverified. No checkbox change, promotion, mint, privileged probe, package
transaction, daemon activation or host remediation was performed. The mkinitcpio42
`/sysroot` upgrade-safety gate remains intact. Tools installed/updated by the
integrator or its reviewers: **none**. Lane-authored files were not edited.
