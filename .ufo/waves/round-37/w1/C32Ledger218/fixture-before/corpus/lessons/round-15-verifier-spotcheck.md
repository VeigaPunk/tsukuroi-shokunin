# Round 15 verifier spot-check — tsukuroi

author: hyaku closure (non-author integrator, @m_strong)

Date: 2026-10-20. Baseline `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`; delivered revision `75d9f4fc1c75841ffe51de5d93b65d4a603d8ffb`. This independent closure did not author or improve the round. Three read-only reviewer seats checked C1 evidence, C2 evidence, and conformance/no-harm; the integrator independently counted committed records, re-opened sources, and ran the required fleet source census. No lane-owned gate, selftest, host package query, build, linter, or formatter was executed by closure. Tools installed/updated: none.

## Closure decision

**status: ok; admitted: true; verdict: admitted.** Both narrowly declared claims verify, and no owned axis is harmed. Counts are re-measured over committed bytes; gate verdicts and selftest tallies are evidence-verified, not re-executed. The dated snapshot is evidence of the recorded observations, not a new observation of this host, a repair, ABI/UI health, running libinput version, or upgrade permission. No exploratory claim or capability acquisition was declared.

## Step-1 conformance

- Fleet command `git log --format='%an %H' -- .ufo/reports/round-15/tsukuroi.md` identifies report commit `7fa305d1ee0820af11bbe986613d8625c1862162`, author `tsukuroi-shokunin`. Its author time is `2026-10-20T05:16:51-03:00`. The filed report names real committed work, all six required sections, evidence, and four `[~]` assessments under `## SHONEN`; it is not a completion marker.
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain` produced no output before this closure artifact. `git ... rev-list --count @{u}..HEAD` produced `0`; HEAD was the delivered revision. `git ... merge-base --is-ancestor <hash> HEAD` succeeded for baseline and each cited round-work commit: `6de977d327a7ee831524cfd6a174ab39c7a07498`, `942fa0a6525cd67a5b7050965b08375676b294cf`, and `75d9f4fc1c75841ffe51de5d93b65d4a603d8ffb`.
- The dispatched `.ufo/prompts/tsukuroi-round-15.md` embeds mission/axes, 1–3 distinct-axis claims, lowest-axis duty, frontier step, batched L2 floor, required report path/sections/SHONEN, commit-before-report and push ordering, hashes, write scope, push scope and L0 channel. Its campaign route aliases are historical dispatch context, not a new authorization to override current session routing.
- One validated 64-seat build wave is durably reported: executor15/scout13/reviewer12/critic8/connector4/scribe4/sentinel4/revenger4; L1 holds the canonical planner seat. No second wave is claimed. The dispatched prompt permitted an optional second wave, whereas the current campaign contract requires falsification when build claims exist; this discrepancy is routed below and does not turn a real report into a marker.
- Dispatch digest copied from the closure prompt (mutable watchdog evidence): `2026-10-20T04:40:41-03:00 launch tsukuroi round=15 pgid=2418552 driver=hyaku-inline attempt=1`; `2026-10-20T05:17:14-03:00 complete tsukuroi round=15; hyaku-inline attempt=1`. The report discloses duration beyond two ticks and lane-owned progression.

## Independent plain measurements

These are counts over committed bytes, not calls into either lane evaluator. The integrator ran this equivalent Python census through the tool kernel, using `subprocess.run` for `git show` and the standard library only:

```python
import subprocess, json, re, hashlib
from collections import Counter
L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
B = '0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2'
A = '75d9f4fc1c75841ffe51de5d93b65d4a603d8ffb'
def show(rev, path):
    p = subprocess.run(['git', '-C', L, 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout if p.returncode == 0 else None
for rev in [B, A]:
    c1 = show(rev, 'corpus/knowledge/source-locator-clarification-r15.json')
    c2 = show(rev, 'corpus/knowledge/partial-upgrade-recheck-r15.json')
    rows = [x for x in show(rev, 'corpus/SOURCES.md').decode().splitlines()
            if re.match(r'^\|\s*S\d{3,}\s*\|', x)]
    cells = [[c.strip() for c in row.split('|')[1:-1]] for row in rows]
    print(rev, len(json.loads(c1)['corrections']) if c1 else 0,
          int(c2 is not None), len(rows), Counter(c[3] for c in cells),
          Counter(c[7] for c in cells), sum(len(c) != 11 for c in cells))
raw = show(A, '.ufo/waves/round-15/build/host-snapshot.json')
snapshot = json.loads(raw)
print(hashlib.sha256(raw).hexdigest(), snapshot['captured_at'])
print(len(snapshot['probes']['pending_updates']['stdout'].splitlines()))
print(repr(snapshot['probes']['package_versions']['stdout']))
```

Observed output, with histogram order normalized for readability:

| Measurement | Baseline | Delivered |
|---|---|---|
| R15 clarification records | 0 (pair absent) | 2: R15-LOCATOR, R15-POSITIVE-DOMAIN |
| R15 update recheck record | 0 (absent) | 1 |
| Source rows | 45 | 49 |
| A/B/C | 37/1/7 | 41/1/7 |
| mined/queued/rejected | 32/5/8 | 36/5/8 |
| Malformed table rows | 0 | 0 |

Separate equality comparison by source ID produced `old_source_rows_changed=0`, `new_ids=['S046', 'S047', 'S048', 'S049']`.

Snapshot output: SHA256 `b101f3747827cefd0ed604c14b669267ec0fcc1b6c2fbe6e486be0cdbbc6ea81`; capture `2026-10-20T07:44:39Z`; pending stdout lines **413**. Package stdout was exactly `libinput 1.32.0-1\nlibinput-tools 1.32.0-1\nmkinitcpio 41.1-1\nsystemd 261.2-1\n`. Both package/pending probes record exit0 and empty stderr. These reproduce the reported values against retained local-sync metadata; they do not re-probe the host.

### C1 / depth — verified, improved

The 0→2 metric is the named R15 pair, not the total number of historical corrections. Both replacement records have an exact 11-word positive definition and stable heading/revision/access-date locators. The prior r14 verifier's two documentation debts are addressed: unqualified reader-line authority is withdrawn, and the unswept negative option-value proposition is superseded by a positive definition. Original r14 content remains history.

Committed `.ufo/waves/round-15/build/verification-fixed.json` names evaluator SHA256 `62859cbb31d3dfbb0ebedf9e5cd684f2bacaa7ff68a69ce7b0dd772f05f271cf`, baseline run exit1/count0/findings7, after run at `942fa0a6525cd67a5b7050965b08375676b294cf` exit0/PASS/count2/findings0, and selftest exit0 **23 cases/23 passed/0 failed**. Before findings include actual historical LOCATOR_UNQUALIFIED and NEGATIVE_DOMAIN_UNSWEPT loci. Original `verification.json` preserves the failed **21/23** selftest rather than laundering it. Read-only review confirms the production prefix/count isolation repair, unchanged expected fixtures, and evaluator/domain-input equality between measured and delivered revisions. The registry in SKILL contains gate type, entry/selftest commands, 0/1/2 mapping, persisted baseline pins, owner and read-only scope. No mutable fleet surface is used by this gate, so the extra mutable-fleet frozen-snapshot obligation is not activated. We verified committed revision-run evidence, not an independently rerun gate.

The lexical gate remains bounded: it cannot establish source truth or exhaustively recognize all possible locator/absence phrasings. Those limits are disclosed and not counterexamples to the shipped source-grounded pair.

### C2 / freshness — verified, improved

The 0→1 dated recheck, 413 pending rows, version fields, snapshot digest and timestamp reconcile with retained bytes. Committed `verification.json` records baseline ABSENT/count0 and implementation `6de977d327a7ee831524cfd6a174ab39c7a07498` COUNTED/count1, health `not_assessed`, decision `BLOCKED_FOR_AGENT_PACKAGE_ACTION`; invalid CLI exit2. The counting probe is correctly registered separately from the verdict gate. Its SHA256 is `6d811c2fe8e551d1d6adc4e81ae4f4671a6e3e1308e3e1e35a59ddc3cf20f875`. Review confirms probe, C2 pair, snapshot and source registry equality across implementation/measured/delivered revisions.

All four older update/health notes have appended named R15-UPDATE-STATE notices, retain their old bytes, and route current use to the new record. SKILL and corpus index also route readers there. The notices prohibit agent package/service actions and distinguish untested future boot-hook risk from an observed boot failure. Two section-number citations in those notices are wrong but the quoted old statements and current-use supersession remain identifiable; route additive corrections below. This does not invalidate the dated recheck or leave the stale statements unmarked.

## Outside discernment spot-check

Sources were re-opened on 2026-10-20. The reader returned ECONNRESET for both Arch manual URLs (including localized retry); `curl --fail --silent --show-error --max-time 45 <URL>` fetched the same canonical URLs successfully, exit0. An in-memory `HTMLParser` extracted text; no source commands were executed. ArchWiki opened directly and identifies revision oldid885170.

| Item from lesson Gate | Decision | Re-opened source | Outside judgment | Reason |
|---|---|---|---|---|
| C1 portable locator and positive ProtectSystem definition; S046 | admit | https://man.archlinux.org/man/systemd.exec.5, SANDBOXING > ProtectSystem=, systemd262.1 | agree | Exact quote: “Takes a boolean argument or the special values "full" or "strict".” It is 11 whitespace words, within25; heading and revision are present. The following full/strict descriptions agree with the replacement. This verifies a newly written SOURCES row, not merely its syntax. |
| Exhaustive parser/undocumented-value conclusion from that definition | reject | Same ProtectSystem entry | agree | The sentence positively documents argument forms; it is not a source-code/parser sweep. The narrower replacement is supported without claiming exhaustive absence. |
| C2 partial-upgrade doctrine; S047 | admit | https://wiki.archlinux.org/title/System_maintenance, Upgrading the system > Partial upgrades are unsupported, oldid885170 | agree | “That is why partial upgrades are not supported.” is an exact nine-word quote. The surrounding dependency/rebuild explanation supports caution, not unilateral repair permission. |
| `--needed` or an all-new target list grants upgrade clearance | reject | https://man.archlinux.org/man/pacman.8, TRANSACTION OPTIONS > --needed; Pacman7.1.0, 2026-10-15 | agree | “Do not reinstall the targets that are already up-to-date.” is exact, nine words. Skipping current targets is not a dependency-closure or partial-upgrade safety guarantee. Print-only target planning does not authorize execution. |
| Package/log observations establish runtime health | reject | Committed host-snapshot.json and partial-upgrade-recheck-r15.json, observations/limits | agree | Retained probes are package database, pending list, filtered log and hooks, not running-library/UI/ABI health probes. The entry explicitly marks that boundary. |

Thus at least one admit and reject were independently sampled and agreed, and newly added S046/S047/S049 source quotes were re-opened. Source recommendations are treated as evidence, not instructions to perform package operations.

## Required source census

Executed by this integrator:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

Exit0, output:

```text
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	W04	S044 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S046 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S049 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

Seven disclosed cross-scope URL warnings; not warning-free and not a failed census.

## Per-axis and trend verdicts

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff 0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2 75d9f4fc1c75841ffe51de5d93b65d4a603d8ffb -- SCORECARD.md` adds the round15 record without rewriting historical scores. PROVINCE and SHONEN are unchanged; the apparent one-line SKILL deletion is the same existing final text receiving a newline before the appended section, not lost instructions. No no-harm conclusion about the live host is implied.

| Axis | Verdict | Evidence |
|---|---|---|
| depth | improved | Two named source-grounded documentation repairs; counted0→2; committed red-before/green-after and23/23 selftest evidence. Ordinal8→8. |
| freshness | improved | One dated snapshot-linked recheck, stale-current-use notices, explicit operator handoff. Ordinal9→9. |
| coverage | unchanged | No new uncovered surface or frontier graduation. |
| operability | unchanged | No capability acquisition; bounded gate/probe support existing documentation work without changing host operations. |
| calibration | unchanged | Explicit bounds and preserved failures; no new calibration claim or score asserted. |
| adjacency | unchanged | Existing OS/mado/operator boundary retained; no absorbed desktop behavior or recovery authority. |

- **expansion: unchanged** — four new source rows curate existing ground, not new knowledge coverage or a capability.
- **quality: improved** — two weaker documentation propositions receive precise replacements, and older update-state records are explicitly marked historical with a dated successor. Small citation defects below do not reverse that strengthening.
- **discernment: improved** — outside r14 debts are converted into lesson-backed QUALITY21/22; this non-author sample agrees on both admits and rejects. Lane-dispatched reviewers are not treated as independent.

## Routed defects and adjudication

1. **tsukuroi, next round — additive citation erratum:** `corpus/knowledge/host-health-report-r3.md:581` says “§1 verdict-board row5”; the actual board is **§0**, row5 at31. Preserve the filed notice and append a named correction.
2. **tsukuroi, next round — additive citation erratum:** `corpus/knowledge/update-safety-v3.md:398` says “§7 rank1”; the quoted “Do nothing now” row is **§5**, row1 at216. Preserve history and append a named correction.
3. **Orchestrator and tsukuroi, next dispatch — falsify-wave contract:** report/lesson claim no second wave required under the old optional dispatched wording. Current campaign requires wave2 when build claims exist. Carry the current requirement consistently into dispatch and execute the bounded attack wave; no retrospective fabricated wave. Status-neutral process debt here.
4. **tsukuroi/orchestrator — execution-scope discipline:** retain the disclosed author-seat deviations (extra ownership/log reads, isolated matcher examples, authoring-time py_compile) and prevent them under future wave no-tests/single-probe instructions. They are not closure-run verification and do not show package/service mutation. The original implementation failure remains visible and repaired.

The reviewer suggestions to treat cramped numeral spacing, duplicate superseded planned bullets, conservative inference labels, or append-only supersession placement as claim failures are not adopted: each is cosmetic or bounded, and source/metric truth remains checkable. Likewise the bounded lexical detector is not claimed to prove arbitrary language/source semantics; no speculative regex expansion is required for this closure.

SHONEN is intentionally unchanged. Not all promotion boxes are independently checkable from this narrow sample: whole-SKILL execution without oral context remains unverified. No promotion, mint, box check, sibling write, host transaction, service restart, or subsequent lane round is authorized or performed by this closure. Existing host-recovery/tooling-policy L0 questions remain operator-owned.
