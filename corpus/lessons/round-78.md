# Round 78 — finite journal path usage and registry discoverability

Base `b9019a1d0558241bf67cf31ff90256284d8657af`; frozen claim commit
`07a607df1a5157daafc91bb5c26858af14415f43`. LOG.md Round 78 motivates
C1 depth (lowest tied, 8), six pinned path-usage examples with review binding,
and C2 operability (9), zero operative registry findings. Neither claims an
ordinal uplift, new coverage or a reusable capability. L1 holds planner.

## Gate

L1 opened both exact upstream URLs on 2026-11-04 before freezing; full files
and SHA256 pins are `before/{journald-manager.c,journalctl.xml,expected.json}`
under `.ufo/waves/round-78/`. Source lines are upstream v262, not installed
Arch build line numbers. ScoutSources and ScribeSources reopened them
independently in-round; their receipts remain author-side evidence.

| Row / candidate | URL, access date, located quote (at most 25 words) | Decision / reason / flip |
|---|---|---|
| S327 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c ; 2026-11-04, :131: `*ret_used += (uint64_t) st.st_blocks * 512UL;` | admit, tier A/code/mined for the scoped function: :119-121 suffix alternatives, :123 no-follow stat, :125 failure skip, :128-129 regular-file guard; six hypothetical contributions, not a live cache reading |
| S328 | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml ; 2026-11-04, :943-944: `This shows the sum of the disk usage of all archived and active journal files.` | reject as sole proof of manager implementation predicates; broad CLI semantics do not specify that implementation. Flip: a located passage expressly specifying those predicates. Contextual documentation is not declared false. |
| Apparent size or symlink-target size determines the function's sum | S327 :123, :128, :131 above | reject: no-follow entry metadata and allocated blocks decide contribution. Flip: a version-pinned implementation with that alternative calculation. |
| Staged adoption / promotion | prior outside closure `round-77-verifier-spotcheck.md:95-100`, prior lesson Sources/frontier | reject while operator-held; flip requires explicit operator release and per-entry gates, not a finite counter pass |

S327/S328 are new rows; no existing row's status, recheck or used-by changed.
S327 scope is distinct from S325's cache arithmetic. S328 remains rejected
for implementation support even where the note cites its contextual manual.

The actual final companion and JSON are integrated byte-exact from
`w1/ScribeNote/{note.md,data.json}`. ReviewUsage's `verdict.json` holds U1-U6
with per-case source reasons, binds JSON SHA256
`13fc82d4cd0756f05b997c7f7a8f64a6976c61aa34d601611a0c73a86a06bd1d`,
and separately records companion SHA256
`f1099591008b0fc8db50a79d72ac9033358dc8af0322816697f2c0a899e98608`.
This is a separate author-side reviewer, not the required outside closure.
Round-78 outside admit/reject spot-check is pending. Round-77 outside check
already agrees on admits and rejects and admits that round; its historical
pending statements are not current verdicts.

## Mistakes

| Class / id | Evidence | Captured-by | Fix shown able to fail |
|---|---|---|---|
| landing — R78-REGISTRY-DEBT | round-77 outside closure routed item 1; round-78 `before/controls.json` C2-do-nothing | QUALITY 70, exact operative registry grammar | Same frozen `check-registry-coverage.py --revision` sees eight missing paths and two incomplete maps, 10 findings/rc1 at the base. Eight reviewed rows and two truthful full row repairs land in the contiguous operative table, not descriptive headings. After receipt supplies the revision-bound comparison. |
| survivor — R78-MISSING-REVIEW | prior outside closure routed item 2; `before/controls.json` scripted-fetch-fill-no-review | QUALITY 81 and 93 | Fresh C1 requires report digest, exact artifact digest, six holds and unique reviewer-role result. Pre-data source-reading fetch/fill without review is 0/rc1; fabricated review without orchestrator result is also 0/rc1. No prior frozen counter is retrofitted. |
| scope — R78-BINDING-NOT-AUTHENTICATION | `w1/CriticFreeze/attack-receipt.json` and `w1/MutationCounter/` | QUALITY 81/89/90; declaration's explicit limit | A complete fabricated report/result bundle can pass; false companion prose also passes the numeric gate. These are isolated adversarial fixtures, not accusations against an actual seat. Source/companion truth is a separate frozen kill rule; the actual reviewed companion explains all branches accurately. This family is not called closed. |
| scope — R78-INSTRUMENT-CHECKOUT | `w1/ReviewRegistry/report.md:9-11` | Gate registry truth, QUALITY 70 | Initial r78 row falsely described only committed reads; corrected row discloses expected specification read from instrument checkout. Initial JT/r74 rows omitted cwd-sensitive --repo and private selftest writes; complete reviewed cells correct both. Existing frozen code is unchanged. |

Pre-data controls: `python3 .ufo/waves/round-78/before/run-controls.py` recorded
15/15 same-reader selftests/rc0, base C1 0/rc1 and C2 10 findings/rc1.
Both do-nothing controls fail their target. The complete fixture expected
values, pins and counter remain fixed after data. The counter is a finite
content/binding instrument, never a universal semantic or authenticity oracle.

## Domain task and source execution

Trigger: journal accounting can be misread from apparent inventory length.
Action: ExecHost reran declared read-only probes and metadata-only inventory,
retained sanitized command/UTC/exit receipts and prepared an operator handoff.
Outcome: `w1/ExecHost/handoff.md` reports systemd 262.1-1, user/root CLI
193.4M, 16 regular matching files, allocated 202866688 bytes versus apparent
268435456 bytes. Exact commands and receipts are under that seat. These are
snapshots, not identical-scope or daemon-health proofs. No cleanup is advised
or authorized; vacuum, rotate, flush, restart and package mutations were not
run. Raw journal contents and machine-id/file names are not retained. The
seat discloses transient full journald configuration capture before its safe
field filter; it is not described as a field-only child read.

ExecSource executes the exact extracted upstream function body on private
real filesystem fixtures. Its six calls cover regular suffixes, wrong suffix,
symlink, directory and a sparse file; they are not the six frozen U1-U6
objects. `w1/ExecSource/receipt.json` records actual stat expectations and
compiler/driver exits. Stat-failure U6 is explicitly NOT EXERCISED by this
supporting harness. Context shims and readdir-error boundary are disclosed;
no installed-binary or arbitrary-error-path equivalence is claimed.

## Registry repair boundary

Eight omitted paths are registered: check-r71-routed-r72,
check-r72-routed-r73, check-r73-routed-r74, check-r75-routed-r76,
count-jd-rows-r76, count-md-rows-r72, count-uf-rows-r74, count-ul-rows-r73.
The existing count-jt-rows-r75/check-r74-routed-r75 rows gain code-2 classes,
explicit --repo and truthful selftest write scopes. ReviewRegistry holds all
final candidate interfaces, separately from numeric coverage. No existing
tool is deleted or modified. No second operative table or duplicate capability
is created. MD and r71-r72 have no selftest mode; r73-r74 conflates failed
selftest and usage under rc2; that historical limitation is explicitly mapped,
not silently repaired or advertised clean. Coverage checks do not execute
commands or certify historical conformance.

The new C1 counter does not import the historical shared revision validator:
its --revision is git-show based and can read any resolvable revision. That
QUALITY27/28 conformance limitation is disclosed; measurements here use full
landed branch hashes, not detached HEAD. The frozen counter is not amended
post-data to claim an untested revision-binding improvement.

## Frontier, reflection and holds

Assimilation: none. Current collision ID lists and indentation control are
retained by ConnectorScope. No staged bytes are adopted, no id renumbering
occurs and no package/promotion hold is considered answered. Latest
`considerthese/2026-10-26.md` was read: counter-attack scoreboard, downstream
patch-offset boundary and correction-propagation map already have lane rules;
no still-unimplemented proposal is claimed newly implemented this round.

This is deeper existing journald ground, not a new coverage-map surface.
README and SKILL add pointers and bounded reading instructions; PROVINCE and
SHONEN remain unchanged. No authority transfer, sibling ownership absorption,
whole-SKILL replay or promotion is inferred. Freshness, coverage, calibration
and adjacency ordinals are unchanged. Outside discernment remains pending.

Canonical PROTOCOL and appendix plus deployment MISSION/AXES/CORPUS/LEARNING
were read before freeze; canonical upstream MISSION/CORPUS/LEARNING copies
were separately reopened after freeze. Their same substantive source, trend
and axis duties are honored, but the exact requested canonical load order
was not fully followed. This is a disclosed process defect, not grounds to
rewrite a frozen predicate. No tool installation or upgrade was needed.

## Wave settlement and recovery

WAVE-DONE w1 was received after all 12 seats settled. One v1 wave, no
residual: scout 1, executors 3, scribes 3, connector 1, reviewers 2,
critic 1, mutation-tester 1. Strict attack share 4/12; no dead seat.
The orchestrator kernel restarted and first retained null outputs for
all seats, despite existing reports. The unmodified null bundle survives
as `w1-results.json.pre-recovery-20261104`. The orchestrator recovered each
row from the seat's actual latest `agent://<id>` output, recording identity,
source/basis/timestamp and a caveat in `w1-results.json`. This is transcript
recovery, not an inferred or rerun vote; no binding rule was relaxed.

ReviewUsage's actual latest output carries
`review_sha256=ed92cb4e52eb2aa5cbdf206eb49e46c9eefa64cdfb06c3bbe658522182d0b66e`,
matching its final verdict file after explicit companion rereview.
ExecRegistry and ScribeNote recovered latest follow-up outputs rather than
their original deliverables; their seat-owned artifacts retain the original
work and updated drafts. Null output alone is not called a dead seat.

MutationCounter's `runner.py`/`matrix.json` records 20 finite probe cases,
two passes, 120 actual CLI invocations including pristine and restored
controls. Fourteen rejection mutants are killed; whole-bundle fabrication
survives as declared. CriticFreeze independently demonstrates accepted false
prose/false review bundles, while reading the actual companion as accurate.
No synthetic verdict is used as the real reviewer result.

ConnectorScope's `source-id-receipt.json` and complete ID-list artifacts bind
base/freeze registry 326 rows, staged 147, base/freeze intersections 127,
working registry 328 and intersections 129. Its indentation control catches
1–3-space exact IDs and excludes code indentation/malformed first cells.
The staged rows with colliding IDs refer to different documents. No package
append is attempted; renumber map is empty. Lists are provided as complete
artifacts rather than a naked count.

## Measured outcome and in-place disclosure

Measured revision `cd71642588c0282a9b73b48f87b415ecdadf6225`.
`after/{before,after}-C1.txt` records 0/rc1 → 6/rc0;
`after/{before,after}-C2.txt` records 10 findings/rc1 → 0/rc0.
`after/commands.json` retains exact invocations; each receipt binds measured
revision, tool revision/digest, stdout and exit. Supporting C1 selftest15/15,
registry selftest23/23 and knowledge refs all rc0. `after/structural.json`
confirms frozen hashes unchanged, zero pre-existing tool deletions/edits,
source rows326→328 and Markdown notes95→96. No ordinal uplift is taken.
Author-side C1/C2 verify on their finite predicates and separate source/
interface reading; outside admission is not self-awarded.

Required census command:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`.
Full start/end stdout and exit0 are in `before/census.txt` and
`after/census.txt`; duplicate-URL warnings are retained, not filtered away.
New rows are A2/B0/C0: one mined, one rejected. No existing status,
recheck or used-by mutation occurred; frontier rows advanced0.

`after/record-sweep.json` contains the exact `git diff -U0` commands and
complete removed-line text for each adjacent commit pair and base→measured,
over SCORECARD, LOG, SKILL, PROVINCE, SHONEN and corpus. Base→freeze removes
0 lines; freeze→integrated removes3 registry rows; base→integrated removes
2 old registry rows. Those three replacement lines are exactly the JT75
row, routed74→75 row and new r78 row disclosed above; all replacements
preserve their tool identity and fix advertised interface/scope. No historical
corpus text is replaced. Later outcome sections add evidence only.

Mandatory fleet-root `git status --porcelain` output is retained in
`after/fleet-status.txt`: no artifact naming this lane/round was found
misrooted. The untracked file `after` contains only `== SCORECARD diff base-`
and provides no lane attribution, so it is left untouched; orchestrator
scratch and other-lane reports are also untouched. No misroot deletion
is claimed. No installation/update was performed by L1 or any seat.
