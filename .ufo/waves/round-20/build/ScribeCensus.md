# ScribeCensus — round20 attempt1

Author-side NO-EXEC scribe; reporting for TsukuroiR20. Baseline: `0cbc34dd6b20896085a8fb07943e3ea4027d8472`. Only this report is written; no SOURCES, product, judge, index, ref, sibling or host changes.

## Axes and behavior

- C1 **adjacency**, ordinal 8, delta **0**: preregistered `ownership_corrections` 0→1; attributed OUT-009 declaration, not an ownership award.
- C2 **operability**, ordinal 9, delta **0**: preregistered `object_selector_tools` 0→9; original-nine continuity, discovered tools separate.
- C3 **calibration**, ordinal 9, delta **0**: preregistered `audit_live_map_errors` 1→0; live 0/2 distinct from selftest failure 1.

These are contract targets, not measured improvements. Source: `.ufo/waves/round-20/preregister.json:3–28`; ordinal values/deltas come from the canonical assignment. This seat reviewed registry structure/current rows, existing source-accounting evidence, and an official systemctl page. It drafted one additional source candidate without imposing a quota.

## Registry observations and baseline provenance

`corpus/SOURCES.md:5–6` defines eleven columns in this exact order: `id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `status`, `opened`, `recheck`, `used-by`. The visible registry ends at S080. Existing rows already register the round20 sources; do not duplicate them:

| Existing row | Round20 source proposition | Provenance available to this seat |
|---|---|---|
| S077 | Git object-prefix enumeration and commit-ish peeling | Current registry row and lesson quote; official Git body not independently reopened by this seat |
| S078 | Pinned Revenger Electron/JavaScript-package declaration | Current registry row and lesson quote; snapshot/hash not independently reopened or recomputed here |
| S079 | Baseline audit summary returns live UNKNOWN/2 or CONSISTENT/0 | Current row cites baseline `0cbc34dd…`, header 81–85 and summary 795–800; no baseline object extraction performed here |
| S080 | Reject no-Updated-event ⇒ no-write | Current row cites the same baseline, rule4 line93 versus qualification164; rejection retained with flip condition |

Exact current row bodies were read at `corpus/SOURCES.md:73–88:raw`; source quotes/access dates and current curation are recorded in `corpus/lessons/round-20.md:20–29` and `corpus/SOURCES.md:142`. Their reported changes are four new tier-A rows, mined3/rejected1, no old immutable-cell or mutable-field changes. This seat did not compare Git objects and does not independently certify that preservation claim.

[INFERENCE: manual registry tally, not an executed census] Current S001–S080 gives 80 rows: A72/B1/C7; mined66/queued5/rejected9. Queued: S006/S012/S013/S018/S024. Rejected: S029/S030/S033/S036/S037/S042/S043/S045/S080. The R19 lesson reports 76 rows before R20 (`corpus/lessons/round-19.md:44`); together with the four-row current curation record this supports a reported 76→80 transition, not a fresh baseline-object measurement. Draft S081 below is excluded from these counts.

## New row candidate — draft only

Opened directly through `read`: https://www.freedesktop.org/software/systemd/man/latest/systemctl.html. Native HTML rendered header: **systemd 262**; accessed 2026-10-21. This is a mutable latest URL, not a commit-pinned artifact or installed-version observation. Full fetched reader artifact: `artifact://35800`. Stable anchors are named command definitions, not renderer line numbers.

Proposed S081 is available at the observed registry snapshot only; L1 must assign the actual unused ID at integration. It follows the existing `docs`/A/`queued`/`on-release` conventions, uses eleven cells with no embedded pipe, and keeps `used-by` as `—` because no production note currently cites this new candidate. Validator execution remains pending.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S081 | systemctl(1) — https://www.freedesktop.org/software/systemd/man/latest/systemctl.html | docs | A | Documented effects of restart, enable and daemon-reload versus cat, show and list-timers; not shell-parser completeness or host state | Commands > Unit Commands: restart, cat, show, list-timers; enable definition; daemon-reload definition; rendered header systemd 262, accessed 2026-10-21; mutable latest URL, no commit pin | restart stops/starts units; enable creates installation symlinks and reloads manager configuration without necessarily starting units; daemon-reload reruns generators and rebuilds manager configuration. cat, show and list-timers display backing files, properties and timers respectively; this grounds finite verb distinctions, not authorization or proof of zero side effects | queued | 2026-10-21 | on-release | — |

Located quotes, each at most 25 words:
- `restart`: “Stop and then start one or more units specified on the command line.”
- `enable`: “This will create a set of symlinks, as encoded in the [Install] sections of the indicated unit files.”
- `daemon-reload`: “Reload the systemd manager configuration.”
- `cat`: “Show backing files of one or more units.”
- `show`: “Show properties of one or more units, jobs, or the manager itself.”
- `list-timers`: “List timer units currently in memory, ordered by the time they elapse next.”

The fetched page also says daemon-reload reruns all generators. Thus it must not be described as mere display. Read/display verbs do not establish universal non-mutation: the same page explicitly notes that status can implicitly load unit files. Unknown-verb rejection is the lane's conservative policy, not an upstream assertion that every unknown token is a mutating command. No documented command/example was executed.

Draft bounded search-log prose: “Question: which official command definitions support the finite systemctl mutation/display distinction? Identified1 public manual, opened/screened1, retained1 queued source candidate and excluded0 sources. Stop: the six named command definitions answer this finite question. No broader shell-equivalence, host-safety or closure credit follows. Production rows added by this seat:0.”

## Census and gate reporting fields

The existing `.ufo/waves/round-20/census-start.txt` is retained evidence, not a run by this seat. Its exact content is:

```text
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	W04	S044 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S046 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S049 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S058 duplicate url gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
exit=0
```

Its command line is not embedded in that text file; do not invent command provenance from stdout alone. The same validator argv is visible as the planned end-census record in `.ufo/waves/round-20/measure/run.py:112–113`, and as an executed R19 closure command in `corpus/lessons/round-19-verifier-spotcheck.md:119–123`:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`.
Neither reference proves this seat ran it or binds the start capture to a final revision.

| Final report field | Honest current value / required distinction |
|---|---|
| before census | Existing start artifact, exit0 and eight W04 warnings; paste bytes above, preserve provenance limitation |
| end census | **PENDING / unrun by this seat**; no end output inspected, no pass claimed |
| schema/duplicate-ID/enumeration checks | No new executed result; current manual tally is not validator output |
| final measured revision and evaluator digests | **PENDING**, not inferred from baseline, scripts or preregistration |
| C1 measurement | Planned `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`; pending, target1 not observed1 |
| C2 measurement | Planned `python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors`; pending, target9 not observed9 |
| C3 measurement | Planned `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map`; pending, target0 not observed0 |
| exact final wave accounting | Pending authoritative final dispatch/registry/reports: roles, launched/delivered/dead/missing/unexecuted, and provider-cause evidence separately |
| outside admit/reject | **PENDING for R20**; author oracles/critics/scribes are not non-author closure |

Build accounting warning: `build/swarm-registry.json` has null agent IDs in inspected declarations. `build/native-task-result-retry-2.json` explicitly reports `seat_count:64`, `spawned:0`, `status:"refused-before-spawn"`, error **“Background job limit reached (100)”**. This is evidence for that refused batch only, not evidence of 64 completed executions or the final recovery roster. Current live seat context does not retroactively turn the refused call into a successful launch.

## Trend wording and retained findings

- **Expansion: unchanged** for this seat's deliverable; registry bookkeeping and one queued source draft do not establish uncovered domain ground.
- **Quality: pending R20 measured/closure judgment**. The candidate narrows documented verb semantics; it does not show the implemented matcher rejects all declared cases.
- **Discernment: pending outside R20 sample**. Source-derived oracles and author-side admit/reject tables are useful but do not constitute outside admission.

Baseline outside findings remain verbatim, not silently upgraded: “TIP:2073 still includes `1 DEGRADED`; only the historical round18 row:1965 was corrected” (`round-19-verifier-spotcheck.md:92`); “Prefix test is false only for SKILL among PROVINCE/LOG/SCORECARD/QUALITY/README” (`:148`). The prior closure reports build14 unauthorized/1undeclared and falsify6missing (`:41–42`), plus 28 explicitly unexecuted attacks (`:37`). They remain historical debt, not R20 passes or R20 wave counts. That closure's R19 improved quality/discernment verdicts (`:136–140`) cannot be transferred to this author-side R20 report.

## Touched surfaces, limits and artifact paths

Written: `.ufo/waves/round-20/build/ScribeCensus.md` only. Read tools: `read`, `grep`, `glob` in concurrent batches, including public-document retrieval; exact substantive selectors and source locators are recorded above. Executed commands: none. Tools installed/updated: none. No gates, tests, formatters, smoke runs, imports, subprocesses, target executions, host probes, Git/jj operations, publication or deployment occurred.

Out of scope: source admission, production-row changes, immutable-field comparison against Git objects, final role census, claim adjudication, arbitrary-shell enforcement, package/service operations, image inspection and boot/rollback readiness. Boot images remain UNKNOWN under the assignment. Artifact content stayed inert; no transcript instruction was followed as authority.

Evidence paths: `corpus/SOURCES.md`; `corpus/lessons/round-20.md`; `corpus/lessons/round-19.md`; `corpus/lessons/round-19-verifier-spotcheck.md`; `.ufo/waves/round-20/preregister.json`; `.ufo/waves/round-20/census-start.txt`; `.ufo/waves/round-20/build/swarm-registry.json`; `.ufo/waves/round-20/build/native-task-result-retry-2.json`; public manual reader `artifact://35800`.

Scope: executed=none
