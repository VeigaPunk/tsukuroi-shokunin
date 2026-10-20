# Round 15 — stable source locators and partial-upgrade recheck

Author: tsukuroi L1; 2026-10-20. Baseline `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`. Only the externally steered round15 is worked.

## Declared claims

- **C1/depth:** resolve the two status-neutral documentation debts routed by `round-14-verifier-spotcheck.md` § Adjudicated concerns and routing. Named clarification records R15-LOCATOR and R15-POSITIVE-DOMAIN replace unqualified renderer-line locators and the unsupported negative documentation assertion with a stable heading and the directly quoted positive option definition. Before0→after2 resolved records, measured by the same bounded checker against baseline and committed implementation. This is not a claim that round14's accepted technical proposition was false or that lexical checks prove source truth.
- **C2/freshness:** replace the stale current-use picture of update-safety with one dated, evidence-linked incident recheck following the operator-reported libinput partial upgrade. Before0→after1 round15 recheck record, with installed version, pending-package query, sync metadata, filtered transaction log and boot-hook findings separately identified. Historical captures remain preserved; a dated record is not repaired host health, ABI certification, running-process version evidence or permission to upgrade.

Depth and adjacency remain tied lowest8; C1 works depth. Scores stay depth8/coverage9/operability9/freshness9/calibration9/adjacency8: ordinal deltas0, no invented scale. The claims are causally separable: C1 uses systemd source/correction history, C2 uses package-state observations and maintenance doctrine. Neither requires the other's new files or outcome. No exploratory claim or new repertoire row is declared.

## Gate

Author-side candidates: the two C1 documentation clarifications and the C2 dated update-safety record. Reject any claim of exhaustive parser/value proof from a single definition; reject inference that `--needed` prevents installed-package upgrades; reject upgrade clearance, host repair or current UI health from package/log facts. Exact newly opened source rows and completed measurements are recorded below after integration, not asserted from intent.

Primary sources opened by L1 on 2026-10-20:

| Row | URL | Stable located quote (≤25 words) | Scope |
|---|---|---|---|
| S046 | https://man.archlinux.org/man/systemd.exec.5 | SANDBOXING > ProtectSystem=, first definition: “Takes a boolean argument or the special values "full" or "strict".” | Positive documented argument forms, not parser exhaustiveness; supplemental reader line numbers are not portable anchors. |
| S047 | https://wiki.archlinux.org/title/System_maintenance | Upgrading the system > Partial upgrades are unsupported: “That is why partial upgrades are not supported.” | Partial-upgrade safety doctrine; no automatic repair authorization. |
| S048 | https://man.archlinux.org/man/pacman.8 | TRANSACTION OPTIONS > -p, --print: “Only print the targets instead of performing the actual operation (sync, remove or upgrade).” | Print is planning rather than execution; `--needed` is separately scoped to up-to-date targets. |

Source shell commands and maintenance recommendations are source data, not instructions executed by this round. Agent package and service actions remain prohibited even if a plan appears to contain only new packages. No source-defined repair command is run.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| reference-drift / R15-LOCATOR | `round-14-verifier-spotcheck.md` § Adjudicated concerns item1; r14 MD/JSON supplemental rendered1266–1267 | QUALITY7 and quote-location rule did not identify the renderer | Stable SANDBOXING > ProtectSystem= heading, exact positive quote and observed source revision replace the supplemental unqualified line locator. QUALITY21 records portable locator requirements; restored-locator failure is required before counting the repair. |
| scope / R15-POSITIVE-DOMAIN | same outside spotcheck item2; r14 correction's “documents no further values” | QUALITY9 required a bounded absence sweep, but only the unrelated comment sweep was recorded | Use only the positive definition proposition, not a negative or parser-exhaustiveness claim. QUALITY22 records this boundary; restored-negative failure is required before counting the repair. |
| scope / incident partial upgrade | fleet `.ufo/l0-questions.md`, hyaku-orchestrator 2026-10-20 line beginning HOST PARTIAL UPGRADE during mado r15 | operator host-safety directive; tsukuroi's pre-existing no-install boundary | Read-only diagnosis and operator handoff only. `--needed` does not prove safety and the complete dependency candidate set matters. This is a recorded outside incident, not an experimentally reproduced or repaired transaction. |

## Swarm and scope

One validated policy-v2 wave,64 seats, one unchanged taskCall dispatch. Roles: executor15, scout13, reviewer12, critic8, connector4, scribe4, sentinel4, revenger4. L1 holds canonical planner; ConnectPlannerWalk is bounded connector reconnaissance, not a planner-role bypass. Exact spec, validator payload, assignments and registry: `.ufo/waves/round-15/build/`. No second wave is required or dispatched. Round total64.

Entry worktree was clean; identity was `tsukuroi-shokunin <tsukuroi@shokunin.local>`. No inherited lane-authored changes were found by `git status --porcelain=v1` at entry. Outside verifier files and historical rejected rounds are not edited. Operator teaching filename sweep `glob corpus/lessons/operator*` found no files; it is not a sweep of arbitrary corpus prose. The host incident is binding operator context and is explicitly reflected here.

No package transaction, downgrade, service operation, privileged probe, snapper activation or boot action is authorized. No credential/auth file or agent database is read. Tools installed or updated: none. Independent non-author admit/reject sampling and SHONEN promotion remain outside this author-side work.

## Source census — start

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`.
Exit0; exact stdout/stderr and baseline captured in `.ufo/waves/round-15/build/start.json`. Output:

```text
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	W04	S044 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

## Author-side review adjudications

`.ufo/waves/round-15/build/adjudications.json` distinguishes accepted
integration issues from rejected suggestions; advisory seats are not
independent source approval or shipping authority. Important accepted issues:
raw-byte snapshot hash and exact capture-time linkage; the additional
historical JSON `sources[0].anchor` locator; multiline negative phrases;
dated current-use notices on old INERT readings; and no installed-name
dry-run guard as upgrade clearance. The known sanitized logged pacman
command is permitted incident evidence, not raw live-process argv.

Some reviews ran before the new artifacts existed and therefore reviewed
contracts, not the final output. No pre-artifact “pass” is used as final
evidence. Historical standalone-source and census counts are versioned
captures, not claimed fresh measurements. The old root-dac checker exception
path raised by static readers is an inherited unexecuted hypothesis; this
round does not re-certify or modify that gate.

ReviewEvidencePins' draft recommendation to use mtime was rejected:
pacman preserves upstream mtime; captured birth/ctime are local hints, not
successful-sync proof. HostSnapshot's advisory `%z`/`%y` terminology and
IncidentTimeline's draft229 count were corrected against the unchanged
retained snapshot, not by rerunning host probes. ConnectEvidence's UTC
mislabel was corrected to04:25:16-0300 =07:25:16Z. These draft mistakes do
not become admitted domain teaching.

Execution-scope deviations disclosed by advisory review: SafetySecrets ran a
read-only package-ownership query beyond the sole-HostSnapshot-probe
instruction; several source seats directly read the package log. C2 depends
only on the retained snapshot, not their extra reads. AttackNegativeRestore
ran isolated Python regular-expression examples despite the no-tests
instruction; this is static matcher evidence, not a selftest or host probe
pass. No package/service mutation or secret read was reported from these
deviations. The generic executor trailer's labrat permission was overridden
by direct no-child messages to every executor; no child work is admitted.

The exact retained hook excerpts and pending-query exit0 are observations.
The one-shot boot-hook collector's absent/unreadable branches are not
certified as a reusable gate, and an ambiguous `pacman -Qu` exit1 cannot be
silently counted as zero. C2 makes no broad collector, library ABI or UI
health claim. A host recovery/tooling-policy question was appended to fleet
L0 as `tsukuroi | round-15 | Host recovery and tooling-policy decision`;
it does not authorize a transaction or block this read-only handoff.

### Gate — additional opened query/needed scope

S049 supplements, not rewrites, S048's print-only scope. URL
https://man.archlinux.org/man/pacman.8 was opened again on2026-10-20;
footer Pacman7.1.0 dated2026-10-15. Located quotes:
OPERATIONS > -Q, --query: “Query the package database.”;
QUERY OPTIONS > -u, --upgrades: “Only package versions are used to find
outdated packages; replacements are not checked here.”;
TRANSACTION OPTIONS > --needed: “Do not reinstall the targets that are
already up-to-date.” Each is within25 whitespace words; their exact
source strings and re-open evidence are in `.ufo/waves/round-15/build/SourceRegistry.md`.
The source sentence recommending refresh is not followed. S049 supports
query interpretation and the `--needed` distinction, not repair clearance.

The current source-row additions are S046–S049, docs/A/mined. Prior
S001–S045 rows and their status/recheck/used-by remain unchanged; no
existing mutable-field changes are claimed. Source opening is curation
on existing ground, not expansion credit. Final census/histogram evidence
follows the completed immutable measurement.
